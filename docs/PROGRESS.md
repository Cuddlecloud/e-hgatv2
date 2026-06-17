# E-HGATv2 — Progress / Handoff Note

Living status doc so any new session (or a VM-attached Windsurf window) can resume with
full context. Pair this with `docs/NEURIPS_PAPER_PLAN.md` (the scientific plan) and the
saved Cascade memories (infra/workflow). To pull the live conversation into a new window,
`@mention` the originating Cascade conversation.

_Last updated: 2026-06-17._

## Where we are
Implementing the NeurIPS plan, currently **Step 4 → Step 6** (the headline Claim 2:
XAI-driven Adaptive Operator Selection works).

- **Step 4 (DONE, in verification):** AOS Channel-B ablation harness.
  - `src/ehgat/benchmark/aos_ablation.py` — 3 arms (`random` / `attention` / `oracle`)
    sharing one NSGA-II skeleton, differing ONLY in `operator_selection`. Per-seed metrics:
    final HV, HV-AUC, IGD+, GD+, spread, evals-to-threshold, wall-clock, evaluations,
    deadlocks. Bootstrap CIs. Serial + ProcessPoolExecutor parallel paths. JSON output.
  - `scripts/run_aos_ablation.py` — CLI entrypoint.
  - `tests/unit/test_aos_ablation.py` — 11 tests (model-free metric tests + e2e smoke on
    exact N=5). **All 11 pass on the pod** with torch 2.6.0+cu124.
- **Step 5 (NEXT):** stats module — Friedman + Holm-Wilcoxon + bootstrap CIs +
  rank-biserial effect size + per-instance P@1 paired test, consuming `aos_ablation.json`.
- **Step 6:** confirm `attention > random`, approaching `oracle` (headline result).

## Currently running on the pod
Headline ablation: `N=10, 30 seeds × 60 gens × 3 arms`, 14 workers, detached via nohup.
- Output: `/workspace/e-hgatv2/experiments/aos_n10/aos_ablation.json`
- Log: `/workspace/e-hgatv2/experiments/aos_n10.log`

## Infra (see also the saved memory)
- **All compute on the RunPod VM**, never the Mac (8-core). Pod = NVIDIA **L40S 46GB**,
  **16 vCPU** (NOT the `nproc=128` the hypervisor reports — cgroup-limited; keep workers ≤14).
- Repo + venv persist at **`/workspace/e-hgatv2`** (only `/workspace` survives relaunch).
  Rebuild after a relaunch: `GPU=1 bash scripts/setup_pod.sh` (idempotent).
- SSH (proxy, interactive-only — pipe commands + `exit`):
  `printf '%s\n' 'cmd' 'exit' | ssh -tt -o IdentitiesOnly=yes -i ~/.ssh/e_hgatv2_instance_ed25519 <user>@ssh.runpod.io`
  (pod host/user change on every relaunch; `id_ed25519` is rejected — use the e_hgatv2 key).

## Remaining plan (high → low)
5. Stats module (Friedman/Wilcoxon/bootstrap/effect size).
6. Run + verify the N=10 AOS ablation (Claim 2).
7. Req2 landscape module (grouped Sobol on exact evaluator + critical-path attribution).
8. Surrogate aggregation ablation (max vs mean vs sum).
9. PGExplainer baseline (faithfulness + optimizer arms only).
10. Scaling matrix N ∈ {10,20,50,100}.
11. **GPU parallelization** (the real N=100 lever given 16 vCPU): batched HeteroData
    inference on the L40S (safe — GPU non-determinism affects only the search trajectory,
    not the exact-CPU-evaluator ground-truth metrics); optional batched GPU max-plus
    evaluator (test-validated against the CPU oracle).
12. Reword Claims 1 & 2 to evidence-backed phrasing; assemble tables/figures from JSON.
