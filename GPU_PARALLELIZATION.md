# E-HGATv2 — Maximum GPU + Parallelization Plan

---
## 0. ⚠️ MEASURED CORRECTION (2026-07-05) — this supersedes §1–§3 below

The plan in §1–§3 was **speculative and wrong on its two headline levers.** I profiled the
actual guided-tape search on an A40 at N=80, both regimes, with per-hot-path wall timers and a
per-function cProfile decomposition (`/tmp/amdahl_timers.py`, `/tmp/amdahl_decomp.py`). Ground
truth:

**(a) Numba on the exact evaluator is useless — 0.2–0.3% of wall-clock, both regimes.**
Even in the coupled regime (event-sim evaluator, 4.7× heavier/call) it is 0.3%. Numba-ing it to
zero saves 0.3%. **DROP lever #7 (§1) entirely.** It was mis-ranked at "5–15×".

**(b) `SEARCH_DEV=cuda` alone HURTS, it does not give "3–6×".** The fused head's makespan runs
`tropical_longest_path` in a **per-node Python loop** (`tropical_dp.py:52-79`) that calls
`.item()` (a GPU↔CPU sync) 2× per node. Over k·pop candidates × N nodes × gens that is
**1.4–4 million syncs**; the profile attributes **68% (uncoupled) / 83% (coupled)** of wall to
`tropical_dp.forward`. On GPU each sync pays kernel-launch latency, so the naive-GPU run was
*slower than CPU*. This is why the earlier GPU N=80 shard projected slower than the CPU sweep.

**The real bottleneck was the per-node tropical DP, called per-graph in BOTH hot paths:**
- offspring **screening** (`tape_predict_objectives`) — k·pop forwards/gen;
- per-gen **guidance** (`tape_signals_batch`→`explain_fused_batch`) — pop forwards+backwards/gen.

NSGA-II sorts (`nsga2.py`) = **0.04s (0.0%)** — irrelevant; do NOT vectorize them.

**FIX IMPLEMENTED (both paths, parity-tested):** route both through the already-existing
layer-vectorised `batched_longest_path` (`tropical_dp_batched.py`) via `build_batch` +
`_forward_batch` (`train_fused_batched.py`). One block-diagonal max-plus DP per chunk; the
Python loop drops from `sum_k N_k` per-node `.item()` calls to `max_k depth_k` vectorised
scatter steps, zero syncs.
- `tape_guidance.py`: `tape_predict_objectives` (screening) + `tape_signals_batch` (guidance)
  now batched; per-graph versions kept as `_tape_predict_pergraph` / `_tape_signals_pergraph`.
- Parity: `tests/unit/test_screening_batched_parity.py` — screening makespan/energy bit-parity
  (both regimes), guidance block-diagonal batch-invariance (both regimes), guidance signal
  bit-parity vs per-graph (coupled). Full unit suite (239 tests) green.

**Measured speedup (profiled search, pop=150, gens=3, N=80, A40):**
| regime | per-graph (orig) | +batched screen | +batched guidance |
|---|---|---|---|
| uncoupled | 254.1 s | 92.5 s | **38.5 s (6.6×)** |
| coupled pp=30 | 438.4 s | — | **44.7 s (9.8×)** |

`tropical_dp.forward` + its millions of `.item()` calls are **gone from the top-15** post-fix.
Remaining cost is the genuinely GPU-friendly GNN encode (~54%) plus pure-Python DAG assembly
(`assemble_coupled_event_dag`, `build_batch_schedule` — no syncs; next tier if ever needed).

**Comparability:** the batched screening is bit-identical to per-graph (makespan/energy), so
screening ranks are unchanged; guidance is bit-identical in coupled and consistent (coupled-DAG
encoding) in uncoupled. A whole-ladder re-baseline through N=160 with the batched path is still
required for internal consistency (as it would be for any GPU move), but the search *behaviour*
is preserved.

**Still valid from §1:** the no-result-change wins (#2 multi-GPU round-robin, #3 train-once
cache, #4 PF\* once, #5 elite carry, #6 single-pass decode) remain worth applying — they're
orthogonal to the DP fix. **Now dead:** #1's "3–6× from a flag" framing and #7 (Numba).

---
## 1. TL;DR max-speed stack

Apply these together, in this order, for the shortest wall-clock at N=160:

1. **Flip the GPU on.** `SEARCH_DEV=cuda` in `scripts/launch_native_overnight.sh:9` (and export before `scripts/run_opt_scaling.sh`). The multi-GPU round-robin (`run_opt_scaling.sh:51-52`, `CUDA_VISIBLE_DEVICES=$((gi % NGPU))`, `NGPU=2`) then activates for free. This moves the per-generation batched GNN screening/attention forward — the O(N^2) cost that explains the measured ~14x jump N=20->N=80 — onto the two idle A40s. **~3-6x whole-shard at N>=80.**
2. **Train the seed=0 surrogate once per instance, not once per shard** (`run_tape_guided_bench.py:163-167`). Cache core+fused state_dicts; 7 of 8 shards load instead of retrain. **No-result-change.**
3. **Compute the seed=1000 PF\* reference once per instance, not once per shard** (`run_tape_guided_bench.py:243-249`), each shard still folds its own local fronts. **No-result-change.**
4. **Carry BRKGA / mp-BRKGA elite objectives** (skip re-evaluating the 20% elite block) — `brkga.py:112,131`, `mp_brkga.py:156,241-242`. **No-result-change** (keep the `evaluations` counter at full P).
5. **Single-pass decode + vectorized bucket/encode** (`decoder.py:89-131`) — 2.9x on `decode()`. **No-result-change** (byte-identical Schedule verified).
6. **`evaluate_objectives` fast-path** (skip the frozen `Evaluation` dataclass + ~11 length-N tuples) — `evaluator.py:236-249`. **No-result-change.**
7. **Then the big refactor:** Numba/array-JIT the exact max-plus evaluator (`evaluator.py:190-234` uncoupled; `:252-451` coupled) with precomputed instance tables. This is the only lever that touches the CPU exact-eval floor GPU screening cannot. **table-clean** (bit-equality regression required). 5-15x on the exact-eval fraction.

**Projected N=160:** uncoupled ~12.7h -> **~2-3.5h** (steps 1-6, all reproducible) -> **~1.5h** (step 7); coupled ~32h -> **~5-9h** -> **~4h**.

Steps 1-6 alone are the recommended first cut: one is a flag, the rest are no-result-change and keep the published table valid.

## 2. The #1 lesson: two A40s sat idle the whole sweep

`scripts/launch_native_overnight.sh:9` hardcodes `export ... SEARCH_DEV=cpu`. Every GNN screening/attention forward therefore ran single-threaded on CPU (`run_tape_guided_bench.py:171-172` moves the model to `args.search_device`, which was `cpu`). **The plumbing is already complete and device-agnostic** — model `.to(args.search_device)`, batched forwards (`attention_nsga2.py:218` `_batch_attention_signals`, `:386` `_predict_objectives`, `tape_guidance.py:125` chunked `tape_predict_objectives`), per-shard GPU pinning (`run_opt_scaling.sh:51-52`), and the faithfulness move-back to CPU (`run_tape_guided_bench.py:276-277`).

**Exact flip:** `SEARCH_DEV=cpu` -> `SEARCH_DEV=cuda` in `launch_native_overnight.sh:9` (keep `NGPU=2`). No code change. Note `--device` is tied to `SEARCH_DEV` at `run_opt_scaling.sh:36`, so core+fused **training** also moves to GPU with the same flag.

**Cost:** this is `quick-look-only` — GPU fp32 reductions differ from CPU in the low bits, changing screening ranks -> different offspring kept -> a stochastically different search trajectory and front. It is NOT apples-to-apples with the published CPU N<=80 cells; publishing GPU numbers requires re-running the entire ladder on GPU (then internally table-clean).

## 3. Ranked optimization table

Ranked by (impact x feasibility). No-result-change + trivial/small first (free wins), then refactors, then result-changing trims.

| # | Lever | Where (file:line) | Technique | Honest speedup (on what fraction) | Effort | Comparability | Already present? |
|---|-------|-------------------|-----------|-----------------------------------|--------|---------------|------------------|
| 1 | Flip SEARCH_DEV=cuda (GPU screening/attention) | `launch_native_overnight.sh:9`; `run_opt_scaling.sh:26,36`; `run_tape_guided_bench.py:171-172` | Move batched GNN forward to A40 | ~3-6x whole-shard at N>=80 (guided arms' O(N^2) screening); ~1x at N<=20; 0 on the 3 exact-eval arms | trivial | quick-look | Yes (flag only) |
| 2 | Round-robin shards across both A40s | `run_opt_scaling.sh:51-52` (`CUDA_VISIBLE_DEVICES=$((gi%NGPU))`) | Process-level data parallel over 2 GPUs | Up to ~2x on GPU-bound throughput when >=2 guided shards in flight | trivial | no-result-change | Yes (auto-on with #1) |
| 3 | Train surrogate once per instance, cache across shards | `run_tape_guided_bench.py:163-167` | seed=0 build_core+train_fused is shard-independent; save/load state_dicts | Removes 7/8 redundant trainings; ~5-15% of a large-N shard, more at small N | small | no-result-change | No |
| 4 | Compute PF\* reference once per instance, cache | `run_tape_guided_bench.py:243-249` | seed=1000 pool is shard-independent; cache, still fold local fronts per shard | Removes 7/8 of ~12-14% reference cost => ~10-13% matrix wall | small | no-result-change* | No |
| 5 | Carry elite objectives (skip elite re-eval) | `brkga.py:112,131`; `mp_brkga.py:156,241-242` | Carry (chrom,obj) for 20% elite block; evaluate only non-elites | ~20% fewer evals on 2/5 arms => ~6-10% whole-shard | small | no-result-change | No |
| 6 | Single-pass decode projection + fold int() | `decoder.py:89,95-100` | Replace 2 nested O(N*(agv+qc)) rescans with one O(N) bucket pass | dominant decode win; combined 2.9x@N160 decode | small | no-result-change | No |
| 7 | Vectorize bucket loops + drop redundant validation | `decoder.py:91-93` (bucket at :56-66) | numpy floor/clamp over the 3N keys at once | ~1.3-1.5x decode standalone; folds into the 2.9x | trivial | no-result-change | No |
| 8 | Vectorize encode_canonical | `decoder.py:123-131` | numpy scatter/arithmetic | 1.6-1.84x encode@N80-160 (byte-identical); slight N=20 regression | trivial | no-result-change | No |
| 9 | evaluate_objectives fast-path | `evaluator.py:236-249` (coupled `:433-451`) | Return (makespan,energy) without frozen Evaluation + tuples | ~5-10% of the exact-eval step | small | no-result-change | No |
| 10 | Cache instance-static node features + gate asserts | `graph.py:60,128,145`; `ehgatv2.py:222` | Memoize [N,4] node tensor + signatures by id(instance); debug-gate assert_graph_semantics | ~3-10% of the 2 guided arms => ~2-4% whole-shard | trivial | no-result-change | No |
| 11 | SEED_OFFSET cross-box scale-out | `run_opt_scaling.sh:45-63` | Offset --seed-start and out-tag so 2 boxes run disjoint seeds | up to ~2x total wall IF a 2nd box exists; fixes tag collision on merge | trivial | no-result-change | No |
| 12 | Concurrency cap + CPU affinity for the ~80 shards | `launch_native_overnight.sh:14-19`; `run_opt_scaling.sh:45-64` | xargs -P / semaphore sized to physical cores, interleave N | ~5-15% if box is oversubscribed; inert on the N=160 tail | small | no-result-change | No |
| 13 | Vectorize crowding distance / rank-crowding | `nsga2.py:124-159` | numpy argsort + neighbour-gap accumulation (fast_nds already vectorized >64) | <2% whole-shard (large pop only) | small | no-result-change | No |
| 14 | Parallelize sample-gen deterministically | `dataset.py:33-45`; `train_fused.py:98-127` | Pre-draw keys=rng.random((num,4N)) then map decode/eval/build over a pool | a few % of whole-shard; keeps sample stream identical | small | table-clean | No |
| 15 | Raise OMP/torch threads on the N=160 tail | `run_opt_scaling.sh:55`; `run_tape_guided_bench.py:44-46` | Let tail shards use >1 thread once short-N done | near-zero (DP is GIL-bound pure-Python); helps only GNN BLAS | trivial | no-result-change | No |
| 16 | **Numba/array-JIT uncoupled max-plus DP + precompute tables** | `evaluator.py:190-234,201-206` | @njit the recurrence over precomputed int/float instance arrays | ~5-15x on uncoupled evaluate() (= ~whole uncoupled-shard CPU); topo-sort residual caps high end | refactor | table-clean | No |
| 17 | **Numba/array coupled event simulator** | `evaluator.py:252-451,348-380` | Integer act ids (task*5+kind), CSR preds/succ, typed min-heap, JIT event loop | ~5-15x on coupled evaluate() (= ~whole coupled-shard CPU); highest correctness risk | refactor | table-clean | No |
| 18 | Batched GPU tropical-DP evaluator (Bellman-Ford [B,N]) | `evaluator.py:173-249` | N max-plus relaxation sweeps over [B,N] tensor for a whole generation | 3-10x on uncoupled-eval fraction after transfer; O(B*N^2) work | refactor | quick-look | No |
| 19 | Vectorize the tropical DP (level-sync scatter-max) | `tropical_dp.py:69-79,91-98` | Layered scatter_max over topo levels; re-derive vectorized backward | ~1.5-2.5x on TAPE head+DP => ~5-12% whole-shard | refactor | quick-look | No |
| 20 | No-grad numpy longest-path fast path (TAPE screening) | `tape_guidance.py:126-135`; `fused_ehgat.py:427` | grad-free numpy DP when `not torch.is_grad_enabled()` (uncoupled only) | ~1.5-3x on TAPE screening => ~3-7% whole-shard; overlaps #19 | small | quick-look | No |
| 21 | Fully batch fused screening head forward | `tape_guidance.py:126-134` | Segmented forward over batch.ptr backed by batched_longest_path | ~1.2-2x on TAPE screening; needs #19 first | refactor | quick-look | No |
| 22 | Batch TAPE head+DP over disjoint-union DAG | `fused_explainer.py:132`; `tape_guidance.py:132` | One block-diagonal DAG per chunk, single DP | ~10-15% on TAPE arm, only after #19; largely subsumed | refactor | table-clean | No |
| 23 | train_fused_batched for the fused head | `run_tape_guided_bench.py:165`; `train_fused_batched.py:218` | Block-diagonal batch, one batched_longest_path/epoch, device=cuda | 2-6x on fused-training (minority of shard) | small | quick-look** | Module exists, not wired |
| 24 | --device cuda core training + large GPU batch | `run_opt_scaling.sh:36`; `train.py:93-164`; build_core batch_size | Move core fit to GPU, raise batch to ~256 with LR scaling | ~1x-few-x on core-fit only (launch-bound at hidden=64) | trivial | quick-look | Flag wired; batch not exposed at call site |
| 25 | Batch/GPU generalization inference | `run_scaling_generalization.py:145-158,186,214` | Batched explain_fused/predict on cuda; drop .cpu() | modest; Amdahl-capped by CPU exact-eval + rho oracle tail | small | quick-look | No |
| 26 | Parallelize arm x seed within a shard (ProcessPool) | `run_tape_guided_bench.py:227-232` | ProcessPoolExecutor over (arm,seed), worker-init stashes instance+models | ~4-5x on an ISOLATED idle-box shard; ~1x/negative on the saturated matrix | small | no-result-change | Pattern in `benchmark/runner.py:241-321`, not here |
| 27 | Process-pool over exact evaluate() (tail-only) | `attention_nsga2.py:926`; `mp_brkga.py:113`; `evaluator.py:173,252` | Persistent pool, instance pickled once, map over offspring | ~1.3-2.5x on eval fraction for isolated large-N; 0/negative on saturated matrix | refactor | no-result-change | No |

\* Reference caching is no-result-change *only if each shard still folds its own local fronts* (`:250-252`). Centralizing the reference to fold ALL shards' fronts (a cleaner PF\*) shifts every hv_ratio and is quick-look — do not mix with existing cells.
\*\* `train_fused_batched` is NOT bit-identical to per-graph `train_fused`: it adds deep supervision over all unroll steps (`train_fused_batched.py:306` vs final-wait-only at `train_fused.py:283`) and grad_clip_norm 5.0 (`:308`). Different weights -> different guidance -> re-baseline required.

## 4. Free wins (flags / no-code or no-result-change)

**Zero code (launcher flags):**
- `SEARCH_DEV=cuda` in `launch_native_overnight.sh:9` — the headline lever (Table #1). Auto-enables the 2-GPU round-robin (#2).
- `SEED_OFFSET` in `run_opt_scaling.sh:45-63` if a second box exists — disjoint seeds, no tag collision (#11).
- `xargs -P`/semaphore concurrency cap in the launchers if the box is oversubscribed (#12).

**Small code, byte-identical numbers (safe to publish):**
- Train-once-per-instance surrogate cache (#3): key on `hash(label, peak_power, core_samples/epochs, fused_samples/epochs, unroll, device)`; atomic write + flock so the ~simultaneous shards don't race the first write; cache in the launcher-matching cpu dtype. The seed=0 hardcoding (`run_tape_guided_bench.py:163,167`) makes every shard's model byte-identical.
- Reference-PF\* cache (#4): cache the seed=1000 pool json per instance; keep the per-shard local fold (`:250-252`) so hv_ratio is unchanged.
- Elite-objective carry (#5), single-pass decode (#6-8), evaluate_objectives fast-path (#9), node-feature cache + assert gating (#10), deterministic sample-gen parallelism (#14).

## 5. Refactors ranked by payoff

1. **Numba/array-JIT the exact evaluator (#16 uncoupled, #17 coupled).** *This is the load-bearing CPU lever.* GPU screening (#1) offloads the guided arms, but the 3 exact-eval arms (mp/sp/random) and every arm's exact-eval survivors stay on the pure-Python max-plus DP (`evaluator.py:190-234`) and heap event-sim (`:348-391`). Precompute per-instance tables (`kinds`, `tau`, `loaded_dist`, `(N+1 x N) empty_dist`, per-speed `1/speed` and `power/speed`) once and `@njit(cache=True)` the recurrence. **Gain:** 5-15x on the exact-eval fraction (~whole CPU cost of a CPU-bound shard). **Effort:** refactor; the topo-sort (`build_precedence` Kahn at `:102-141`) is a residual unless also arrayified. **Correctness:** MUST pass bit-equality vs current `_evaluate_uncoupled` on the N<=80 golden schedules (float max/+ and sum order must match); the coupled sim must reproduce the tie-break key (`avail, task_id, empty-before-loaded` at `:366`), the `power_used<=p_max+_EPS` admission (`:370`), the `t>avail+_EPS` arc emission (`:376`), and the +_EPS batch-pop (`:394`) exactly. table-clean once parity holds.
2. **Batched GPU tropical-DP evaluator (#18).** Alternative to #16 for the uncoupled path: N Bellman-Ford relaxation sweeps over a `[B,N]` tensor for a whole generation. **Gain:** 3-10x on the uncoupled-eval fraction. **Effort:** refactor + host<->device transfer per gen; O(B*N^2) work. **Correctness:** bit-identical only in float64 with the exact per-node recurrence; any fp32/reassociation shifts fronts -> quick-look. *Recommendation:* prefer #16 (Numba) — no build/transfer overhead, no GPU dependency, and the pure-Python block-diagonal build in `tropical_dp_batched.py:51-87` would be re-paid every generation (this is why wiring `batched_longest_path` into `evaluate()` was REJECTED — it relocates the bottleneck).
3. **Vectorize the tropical DP for the TAPE head (#19)** + **no-grad numpy screening fast-path (#20).** These remove the per-node Python loop + per-node `.item()` in `tropical_dp.py:69-98` that (a) is the biggest per-graph Python hotspot and (b) makes CUDA a *regression* for the TAPE arm today (every `.item()` forces a host-device sync). Do #19 or #20, not both fully (they remove the same loop). **Gain:** ~5-12% whole-shard. **Correctness:** scatter_max GPU tie index is undefined — must reproduce "first maximum in edge order" (tie-break by min edge id) or the critical-path Jaccard/TAPE gradients shift.
4. **Batch the TAPE head+DP over a disjoint-union DAG (#21, #22).** Only pays *after* #19 (with a per-node Python DP, unioning graphs doesn't cut the loop count). Removes per-graph dispatch. **Gain:** ~10-15% on the TAPE arm on top of #19.
5. **Process-pool parallelism (#26 arms, #27 evaluate).** Genuine only on an *isolated idle-box* single shard (e.g. a lone N=160 run): ~4-5x (#26) / ~1.3-2.5x (#27). On the saturated ~80-way matrix they OVERSUBSCRIBE and net-lose — gate behind `shard_count < cores`. Pick ONE axis (arm-level #26 is coarser and avoids per-eval pickling; #27 is finer and enlarges the eval batch). Must pair with search-device=cpu (fork+CUDA is unsafe) — so #26/#27 and #1 are mutually exclusive per process; dedicate GPUs to guided shards and pools to the exact-eval tail.
6. **train_fused_batched (#23) + GPU core training (#24).** Training is a minority of a large-N shard and #3 already removes 7/8 of it, so residual payoff is small; both change weights -> re-baseline. Low priority.

**Do NOT implement (verified net-negative / rejected):**
- **AMP/fp16 autocast** — hidden=64 tiny matmuls are launch-bound, not tensor-core-bound; fp16 rounding can flip the max-plus critical-path tie and corrupt the faithfulness signal.
- **torch.compile** — variable per-generation candidate counts trigger recompiles; the Python DP graph-breaks.
- **CUDA graphs** — post-screening shapes vary every generation; capture needs static shapes.
- **decode_batch** (`decoder.py:69`) — the ragged nested-tuple construction is the floor and doesn't vectorize; net SLOWER than the scalar rewrite (#6-8).
- **Memoize decode/evaluate by chromosome key** — crossover_prob=0.9 x mutation_prob=0.9 => ~1% clone rate; hashing 4N float64s per call is strictly added cost with ~0 hits.
- **Warm-start incremental DP** — ~90% of offspring are fresh random-key re-decodes with no parent; speed mutations still force full coupled re-propagation.
- **Batched block-diagonal tropical DP wired into evaluate()** — relocates the bottleneck (pure-Python build re-paid every gen); Numba (#16) strictly dominates.

## 6. Concrete implementation order (phased)

**Phase 0 — flip the switch (minutes, quick-look):**
Set `SEARCH_DEV=cuda` in `launch_native_overnight.sh:9`. Run a CPU-vs-CUDA parity check on the surrogate screening rank at a fixed seed; if kept-offspring sets match, treat as table-comparable, else mark GPU cells as a separate config. This alone is the ~3-6x whole-shard cut at N>=80.

**Phase 1 — free reproducible caching (1 day, no-result-change):**
Implement #3 (train-once cache), #4 (reference cache with per-shard local fold), #5 (elite carry, keep evals counter). These stack multiplicatively with Phase 0 and keep the published table valid. Add the atomic-write + flock so concurrent shards don't race.

**Phase 2 — no-result-change micro-wins (1 day):**
#6-8 (decode/encode vectorization), #9 (evaluate_objectives), #10 (node-feature cache + assert gating), #13 (crowding). Repoint `brkga.py:67`, `mp_brkga.py:114`, `attention_nsga2.py:926` to `evaluate_objectives`. Verify byte-identical Schedule/objectives on the golden N<=80 fixtures before merging.

**Phase 3 — the CPU floor (1-2 weeks, table-clean, biggest structural win):**
#16 (Numba uncoupled DP + precompute tables) first with a bit-equality regression vs current evaluator on N<=80 golden schedules; then #14 lets `generate_graphs` inherit it. Then #17 (coupled event-sim) with the exhaustive parity harness (including the "reduces to uncoupled at large peak_power" property test). Only after parity passes do these feed table cells.

**Phase 4 — GPU DP + tail parallelism (optional, quick-look):**
#19/#20 (vectorize tropical DP so CUDA stops regressing the TAPE arm), #21/#22 (batch the head). For lonely end-of-sweep N=160 shards on an otherwise-idle box, enable #26 or #27 gated on `shard_count < cores`.

**Re-baseline gate:** if any quick-look lever (Phase 0, #18-25) is used for publication, re-run the *entire* N-ladder on one device — never mix with CPU N<=80 cells.

## 7. Estimated before/after N=160 walltime (with Amdahl reasoning)

**Before (measured, CPU-only):** unc N=20 873s, N=40 3396s, N=80 12404s => ~3.7x/doubling (~N^1.89, i.e. O(N) DP x O(N)=20N pop/gen). One more doubling: **unc N=160 ~= 12.7h** (12404 x 3.7 ~= 45,900s). Coupled ~2.5x uncoupled => **coupled N=160 ~= 32h**. Total sweep is tail-bound by this coupled shard.

**The Amdahl fork (be honest — the subsystems disagree):**
- The "full GPU stack" analysis attributes the ~14x N=20->N=80 jump to GNN screening being O(N^2) and ~85-95% of a shard at N>=80. If true, GPU screening (#1) alone is a ~5-10x whole-shard lever.
- The "search loops" analysis says the pure-Python exact `evaluate()` (~2ms/eval, ~4e5/shard) is the dominant common cost across all 5 arms. If true, GPU screening caps near 1/(1-0.3) ~= a few x, and the Numba evaluator (#16/#17) is the real lever.
- Reality is between: screening dominates the 2 guided arms (which is where the N^2 shows up); exact eval dominates the 3 non-guided arms + guided survivors. So **GPU screening (#1) is bounded by the CPU-only arms** (mp/sp/random ~228s/seed at N=160, unaffected).

**After — free stack (Phases 0-2, mostly reproducible):**
- #1+#2 GPU screening on both A40s: ~3-6x whole-shard at N=160.
- #3+#4 caching: removes ~10-15% redundant train+reference from the CPU work.
- #5+#6+#9+#10: ~1.2-1.4x on the CPU floor.
- Stacked: **unc N=160 ~2-3.5h** (from 12.7h), **coupled ~5-9h** (from 32h).

**After — with the evaluator refactor (Phase 3, table-clean):**
- #16/#17 give 5-15x on the exact-eval fraction that GPU cannot touch. Once both the guided arms (GPU) and the exact-eval floor (Numba) are fast, the shard is bounded by whichever residual is larger.
- **unc N=160 ~1.3-1.8h; coupled ~3.5-5h.**

**Total sweep:** tail drops from ~30-34h to ~5-9h (free) / ~4h (with JIT), plus the concurrency cap (#12) trims bulk-phase thrash.

## 8. Comparability guardrails

**Safe to merge with the published CPU N<=80 cells (no-result-change / table-clean, verified byte-identical or bit-parity-gated):**
- #3 train-once cache (seed=0 model is byte-identical), #4 reference cache *with per-shard local fold*, #5 elite carry (deterministic pure function; keep the evals counter), #6-8 decode/encode (byte-identical Schedule/keys verified), #9 evaluate_objectives, #10 node-feature cache, #11 SEED_OFFSET (disjoint seeds, CIs recomputed from pooled raw arrays), #12/#15 scheduling, #13 crowding (gate behind a diff test — tie-break stability at `nsga2.py:158` must be preserved), #14 sample-gen (pre-drawn keys keep the stream identical), #26/#27 process pools (order-independent), #16/#17 Numba evaluator (table-clean **only after** the bit-equality regression passes).

**Quick-look-only — breaks apples-to-apples, requires a full one-device re-baseline:**
- #1 SEARCH_DEV=cuda (fp32 GPU vs CPU reorders screening ranks -> different offspring kept -> different trajectory AND GPU-trained weights differ), #18 GPU batched evaluator (fp32/reassociation shifts fronts unless float64), #19-22 GPU/vectorized tropical DP (scatter_max tie index), #23 train_fused_batched (deep supervision + grad clip -> different weights), #24 GPU core training + large batch (optimizer trajectory changes weights), #25 generalization inference.
- Reference-PF\* *centralization* (folding all shards into one PF\*, as opposed to caching + per-shard local fold) shifts every hv_ratio — quick-look.

**Rule of thumb:** anything that moves a float reduction onto the GPU or reorders it is quick-look; anything that only skips redundant deterministic work or reshapes CPU control flow with a parity test is table-clean.

## 9. Open risks / what could still be slow

- **The Amdahl split is unmeasured on GPU** (this box reports `cuda=False`, no `nvidia-smi`). The ~3-6x from #1 is code-inferred from the N^1.89 scaling, not benchmarked. First action on the VM: profile one N=80 guided shard CPU-vs-GPU to fix whether screening or exact-eval dominates.
- **CUDA can REGRESS the TAPE arm** until #19 lands: `tropical_dp.py:69-79` does `torch.argmax(...).item()` per node; on CUDA every `.item()` is a host-device sync. Consider keeping the TAPE arm on CPU (or dedicating a GPU worker) until the DP is vectorized.
- **The coupled event-sim (`evaluator.py:252-451`) does not vectorize** (power-budget greedy admission is inherently serial). Only #17 (Numba) helps it, and it carries the highest parity risk of the set (coupled makespans *and* TAPE power-arc training targets derive from it). Coupled N=160 stays the sweep tail until #17 is proven bit-for-bit.
- **build_precedence / build_hetero_graph residuals:** the Kahn topo-sort (`evaluator.py:102-141`) and the per-task `_agv_arc_features` physics loop (`graph.py:111-117`) stay pure-Python after #16 and become the next Amdahl wall; they are schedule-dependent and not cacheable.
- **Oversubscription:** never enable intra-shard pools (#26/#27) under the ~80-way launcher — it thrashes. They are strictly tail-of-sweep levers on an idle box.
- **Cache footguns:** the surrogate/reference cache keys MUST include every training/reference-affecting arg + a code-version tag, or a config change silently loads a stale model; add an assert on the config hash and an atomic write + flock for the racing concurrent shards.
- **The merge inconsistency is orthogonal and unfixed:** `merge_tape_shards.py:72-80` reports only recs[0]'s ref_hv against pooled per-seed hv_ratios; reference caching (#4) does not fix this latent mismatch.