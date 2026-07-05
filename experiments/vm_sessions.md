# VM session log (ephemeral compute)

Every heavy E-HGATv2 run goes on a rented ephemeral VM. Log hardware here before teardown
(the box disappears; the numbers must survive in git).

## 2026-07-05 — vast.ai RTX PRO 6000 WS

- **GPU:** 2× NVIDIA RTX PRO 6000 Blackwell Workstation Edition, 96 GB each (97887 MiB), driver 595.71.05
- **CPU:** 512 vCPU (~256 physical cores)
- **RAM:** 372 GB (≈281 GB free at start)
- **CUDA:** 13.0 (nvcc V13.0.88), driver 595
- **Disk:** 1.8 TB overlay (~407 GB free)
- **Lease:** ~6 h, $2.196/hr, Colorado
- **Env:** fresh Ubuntu (Python 3.12.3, numpy only) → venv at `/workspace/venv`, **CPU torch 2.12.1** (sweep is CPU-bound; guided arms + exact-eval baselines both run on CPU), PyG 2.8.0, ehgat installed editable.
- **Repo:** local HEAD `6a294f1` (batched tropical-DP refactor) is local-only (not on origin); working tree rsynced to `/workspace/e-hgatv2`.

**Why CPU torch, not the GPUs:** the ladder sweep is embarrassingly parallel across
seed×N×regime shards (single-thread each). With ~256 physical cores all shards run
concurrently, so wall-clock = the single slowest shard. The 2 GPUs cannot beat that: the
exact-eval baselines (mp-BRKGA / random-NSGA — the stall arms) are CPU-only by construction,
and routing the guided arms through 2 GPUs would serialise work the cores otherwise run
~256-wide. GPUs only help single-shot latency (profiling / guided-only runs).
