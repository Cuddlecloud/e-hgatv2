# E-HGATv2 — Progress / Handoff Note

Living status doc so any new session (or a VM-attached Windsurf window) can resume with
full context. Pair this with `docs/NEURIPS_PAPER_PLAN.md` (the scientific plan) and the
saved Cascade memories (infra/workflow). To pull the live conversation into a new window,
`@mention` the originating Cascade conversation.

_Last updated: 2026-06-17._

## Key findings so far (Claim 2 investigation)
1. **N=10 ablation, Channel-B isolated (screening off), old design** -> **null**: random/
   attention/oracle HV are statistically indistinguishable (all Holm-Wilcoxon p > 0.05;
   attention-random HV median -11.6k, p=0.74, r=-0.25). So the prior "H2 win" is driven by
   **Channel-A task selection + surrogate screening**, not operator-type routing.
2. **Diagnostic refuted the washout hypothesis**: the bottleneck signal is sharp AND
   correct -- attention agv_bias 0.90 ~ oracle 0.84, both correctly find the **AGV** is the
   dominant bottleneck (2 AGVs vs 3 QCs). Strong support for **Claim 1 (faithfulness)**.
3. **Root cause of the null = operator crowd-out**: at high agv_bias the old
   `_SPEED_BASELINE=0.5` pushed the `speed` operator BELOW the uniform 1/4 share, starving
   the makespan<->energy lever that generates HV spread. **Fix:** `speed` score is now a
   configurable `operator_speed_weight` (default 1.0, >= structural ops).
4. **Redesign helped but is still a tie at N=10**: attention HV -1.6% -> -0.6% vs random;
   oracle -0.3%; HV-AUC flipped (oracle 0.713 > random 0.707). Still ns -- N=10 is too
   small (AGV is always the bottleneck; random already covers the tiny operator space).
5. **=> Scaling is the real test.** Redesigned ablation running at N=20 and N=50, where the
   AGV/QC structure is richer. (`scripts/diagnose_aos_bias.py` reproduces finding #2.)

## Where we are
Implementing the NeurIPS plan, currently **Step 4 → Step 6** (Claim 2). Step 5 (stats)
DONE. Investigating whether Channel-B operator routing helps at scale (#5 above).

- **Step 4 (DONE, in verification):** AOS Channel-B ablation harness.
  - `src/ehgat/benchmark/aos_ablation.py` — 3 arms (`random` / `attention` / `oracle`)
    sharing one NSGA-II skeleton, differing ONLY in `operator_selection`. Per-seed metrics:
    final HV, HV-AUC, IGD+, GD+, spread, evals-to-threshold, wall-clock, evaluations,
    deadlocks. Bootstrap CIs. Serial + ProcessPoolExecutor parallel paths. JSON output.
  - `scripts/run_aos_ablation.py` — CLI entrypoint.
  - `tests/unit/test_aos_ablation.py` — 11 tests (model-free metric tests + e2e smoke on
    exact N=5). **All 11 pass on the pod** with torch 2.6.0+cu124.
- **Step 5 (DONE):** `src/ehgat/benchmark/stats.py` + `scripts/run_aos_stats.py` +
  `tests/unit/test_stats.py` (14 pure numpy/scipy tests, pass on pod) — Friedman +
  Holm-Wilcoxon + rank-biserial + bootstrap CIs over `aos_ablation.json`.
- **Step 6 (in progress):** does Channel-B beat random at scale? (N=20/50 running).

## Two redesigns of Channel-B (both implemented)
1. **speed-weight fix** (`operator_speed_weight`, default 1.0): stops `speed` crowd-out.
   Scale results (scalar/population bias): N=10 -0.6%, N=20 **-2.5%** vs random, all ns.
   The N=10->N=20 worsening = the population-AVERAGE is the real flaw.
2. **per-task routing** (`operator_granularity=per_task`): route each mutation from the
   chosen task's OWN bottleneck (attention `w_agv[j]/(w_agv+w_qc)` via fused single-pass
   `_attention_signals`; oracle exact critical-path membership). Cost-neutral. Being tested.

## Experiment map (experiments/)
- `aos_n10/` old null (sw=0.5, population). `aos_v2_n{10,20,50}/` sw=1.0, population.
- `aos_pt_n{10,20,50}/` sw=1.0, **per_task** (the new mechanism).
- Compare: per_task attention-vs-random AND per_task-vs-population at each N.
- Analyse any: `python scripts/run_aos_stats.py --input experiments/<dir>/aos_ablation.json`

## Currently running on the pod
- Scalar/population scale chain (PID 3134): N=50 in progress (`aos_v2_n50.log`); N=10/20 done.
- **Queued** per_task chain (PID 4881): waits for 3134, then runs `aos_pt_n{10,20,50}`.
- Check: `ps -p 3134; ps -p 4881; grep -c AOS.progress experiments/aos_*_n*.log`

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
