# Compute Scaling — GPU/CPU Parallelizability of the E-HGATv2 Pipeline

> How the optimization/search pipeline uses (and fails to use) the A40 GPUs and the 255-core
> CPU, what the codebase already supports, and the concrete levers to make the R3 optimization
> comparison tractable at the advisor's full range (**N up to 160**, the DL benchmark size).
> Numbers measured on the vast.ai box (2× A40 46 GB, 255 cores) on 2026-07-03.

## TL;DR verdict
- The earlier "N=160 optimization takes days / O(N²)" fear was **wrong**. The exact max-plus
  evaluator is fast (see below), so the exact-eval arms (mp-BRKGA, random NSGA-II, single-pop
  BRKGA) are cheap even at N=160.
- The real cost at large N is the **GNN offspring-screening of the guided arms running on CPU**.
  The search code **already** batches those forwards onto the model's device — so simply
  keeping the surrogate on **CUDA** (instead of `.cpu()`-ing it) moves that cost to the A40.
- Net: **N=160 is feasible**, not intractable. The lever is GPU for the guided arms + the
  fact that the exact-eval baselines are already cheap.

## Measured costs (N=160, matched budget P=5N ⇒ base_pop=800, matched_pop=3200)
| Quantity | Value | GPU-able? |
|---|---|---|
| Exact evaluator throughput @ N=40 | **4883 evals/s** (0.20 ms/eval) | No (sequential max-plus DP, CPU) |
| Exact evaluator throughput @ N=160 | **1259–1321 evals/s** (0.76–0.79 ms/eval) | No |
| mp-BRKGA, N=160, **full 40 gens, 1 seed** | **≈228 s (< 4 min)** | Already cheap (CPU exact only) |
| Guided (TAPE/attn) GNN screening @ large N | CPU-bound bottleneck | **Yes** — batched onto model device |

The mp-BRKGA/random/single-pop arms each do ~128k exact evals per seed at N=160 (3200/gen ×
40 gens) ⇒ ~100 s of pure evaluation. The guided arms do the same exact evals **plus** the
screening forwards; on CPU the screening dominates, on GPU it is a batched launch.

## What the codebase ALREADY does to facilitate parallelism

### GPU (surrogate forwards)
- `src/ehgat/search/attention_nsga2.py::_batch_attention_signals` — batches **every** candidate
  schedule's hetero-graph into **one** `model.attention(batch.to(device))` call per generation,
  on `next(model.parameters()).device`. Comment: *"one ~10k-graphs/s GPU launch instead of G
  serial ~10-graphs/s CPU forwards."* So attention-guided screening is GPU-native when the model
  is on CUDA.
- Same file, offspring **screening** path (`model.predict(batch.to(device))`) — the surrogate
  regression used to screen `k·λ` offspring down to `λ` is also a single batched device forward.
- `tape_signals_batch` / `tape_predict_objectives` (TAPE guidance) follow the same batched form.
- **`run_attention_nsga2` needs no device argument** — it simply runs on whatever device the
  passed model lives on. Put the model on `cuda` ⇒ the search screening runs on the A40.
- Training already accepts a device: `build_core(..., device=...)`; the fused head trains on
  the core's device.

### CPU (independent jobs across cores)
- The established pattern is **process-level fan-out across the 255 cores**, one independent job
  per (instance, seed-shard), each pinned to a single BLAS thread (`OMP_NUM_THREADS=1`):
  - `scripts/run_tape_matrix_sharded.sh` — 11 instances × seed-shards, all concurrent, merged by
    `scripts/merge_tape_shards.py`.
  - `scripts/run_opt_scaling.sh` — the N-ladder, seed-sharded (this study).
  - `scripts/run_front_parallel.sh` — `xargs -P` per-instance front caching.
- `run_tape_guided_bench.py` exposes `--seed-start` + `--out-tag` + `--out-dir` precisely so seeds
  can be split into parallel shards and merged afterward.

## What currently FORCES CPU (and how to change it)
- **`run_tape_guided_bench.py` calls `fused = fused_res.model.cpu()` and `core = core.cpu()`**
  right after training (≈ lines 155–156), then runs the search — so every arm ran on CPU even
  when a GPU was present. The `--device` flag only affects **training**; the comment even says
  *"search runs on cpu."*
  - **Fix:** add a `--search-device {cpu,cuda}` option (or reuse `--device`) and skip the
    `.cpu()` when it is `cuda`, so the guided arms screen on the A40. One-line-ish change;
    the search code needs nothing else because it already honours the model's device.

## Levers to reach N=160 (ranked)
1. **Keep the surrogate on CUDA during search** (above). Moves the guided-arm screening cost to
   the A40; the exact-eval baselines are already cheap. *Biggest, lowest-risk win.*
2. **Seed-shard across cores** (already used). At N=160 each seed-shard of mp/random/sp is a few
   minutes; run all shards + regimes concurrently on the 255 cores.
3. **Two A40s** — pin different shards/regimes to `CUDA_VISIBLE_DEVICES=0` vs `1` to avoid a
   single-GPU queue when many guided shards run at once.
4. **(Optional, larger change) Parallelize the population fitness eval within a run.** The
   per-generation `evaluate()` calls are embarrassingly parallel; a process pool over the
   population would cut the exact-eval wall further. Not currently implemented and not needed
   given (1)+(2), but it is the path if the ladder ever goes well beyond N=160.
5. **(Not worth it) GPU the exact evaluator.** The max-plus longest-path DP is sequential per
   schedule; vectorizing it across candidates is a real rewrite for little gain since it is
   already sub-millisecond per eval.

## Recommended config for the N=160 optimization sweep
- Models on **CUDA** for the guided arms (`--search-device cuda`), exact-eval arms on CPU.
- Budget-matched P=5N (matched_pop=20N), gens=40 — same as the main table, so points reconcile.
- Seed-shard (e.g. 8 seeds × 2/shard) across cores; split regimes across the two A40s.
- Ladder N ∈ {10, 20, 40, 80, 160} to cover the advisor's DL range.
