# E-HGATv2 — Progress / Handoff Note

Living status doc so any new session (or a VM-attached Windsurf window) can resume with
full context. Pair this with `docs/NEURIPS_PAPER_PLAN.md` (the scientific plan) and the
saved Cascade memories (infra/workflow). To pull the live conversation into a new window,
`@mention` the originating Cascade conversation.

_Last updated: 2026-06-20._

## Physics-unrolled GNN+TAPE — closes the coupled makespan gap (NEW, 2026-06-20)
**Problem.** Under peak-power coupling the per-leg wait is a *timing fixed-point* (it depends
on which legs run concurrently, which depends on the waits). A single static wait head caps
coupled makespan R² at ~0.80 (vs 0.997 uncoupled). Static global-context pooling did not help.

**Fix (implemented).** `FusedEHGATv2` now runs `unroll_steps` (K) physics-unrolled refinements
in coupled mode — a learned, differentiable analogue of the simulator's contention resolution.
Each step: (1) wait head predicts per-leg waits, (2) the max-plus DP recomposes the tentative
timing, (3) per-leg **contention features** are read off that timing, (4) they feed the next
wait prediction. Both modules fire every step — the GNN supplies the nonlinear waits, TAPE
supplies the timing the next GNN step needs; neither can be removed.
- Contention feature (`_peak_contention`, shared per-graph + batched): the **peak instantaneous
  concurrent power** over a leg's active interval (the exact quantity the simulator's
  `power_used + p <= budget` rule gates), plus concurrent-others power, budget excess, peak
  concurrent leg count. Budget-normalised and **bounded** (clamp `_CONT_CLAMP=6`) so the
  feature scale is stable in N and cannot blow up the feedback. Computed from *detached*
  previous-iterate timing (truncated/Gauss-Seidel: gradients flow only through the final
  composition). Wait head output layer is **zero-initialised** (starts at the mean wait).
- Batched trainer mirrors it exactly (`_batched_contention`, per-sample-blocked since N is
  constant within an instance; scales to the val batch). Grad-norm clip 5.0.
- Wired through `FusedTrainConfig.unroll_steps` and `scripts/run_fused_eval.py --unroll-steps`.

**Result (coupled pp=30, 10 seeds, A100; R²_makespan, leg-Jaccard intact ~0.92–0.95):**
| K | N=6 | N=10 | N=20 |
|---|-----|------|------|
| 0 static | 0.861 | 0.801 | 0.800 |
| 1        | 0.882 | 0.854 | 0.865 |
| 2        | 0.880 | 0.857 | 0.868 |
| 3        | 0.880 | 0.858 | 0.870 |
Lift +0.06–0.07 at N=10/20, **growing with N** (coupling matters more at scale); stable across
all seeds after the clamp. K=1 already captures most of the gain (cheapest); K=3 marginally best.
Tests: `tests/unit/test_fused_batched.py` (K=0 legacy, vectorised contention == per-graph,
uncoupled reduction).

**Size transfer (the scaling claim) — `scripts/run_unroll_transfer.py`.** Train on small N
(exact event-sim labels), predict coupled `(C_max,E)` **solver-free** on larger unseen N, no
retraining. Trained on N=10, pp=30, 8 seeds (R²_makespan, zero-shot):
| test N | K=0 static | K=2 unrolled |
|--------|-----------|--------------|
| 10 (in-dist) | 0.796 | 0.863 |
| 15 | 0.802 | 0.870 |
| 20 | 0.737 | 0.846 |
| 30 | 0.573 | 0.800 |
| 40 | 0.461 | 0.779 |
The **static head collapses** with N (0.80→0.46: it memorises N=10 wait magnitudes); the
**unrolled model transfers** (0.86→0.78) and the gap **widens with N** (+0.07 @N=10 → +0.32
@N=40) -- it learns the contention-*resolution mechanism*, not the magnitudes. MAE @N=40:
88s (unrolled) vs 145s (static). Solver-free forward is 21-81x faster than the simulator
(grows with N; far larger vs CP-SAT labels). Energy transfers exactly (additive, R²=1.0).
**v2 upgrade (richer features + deep supervision, 2026-06-20).** `_peak_contention` now emits
6 per-leg features (added: start-time **rank** = queue position, and **time-to-next-budget-free**
= soonest a concurrent leg finishes after this leg's start, the quantity that sets the wait
length) -- encoding the priority/queue structure the simulator's SGS uses, not just the power
summary. Training adds **deep supervision**: every unroll step's waits are supervised toward
`wait_true` (`wait_steps` stacked from `_forward_batch`), so the iteration converges to the
fixed-point. Result (K=2): in-dist N=20 0.868->**0.874**, N=10 0.857->0.868; transfer N=40
0.779->**0.819**, N=30 0.800->0.832 (gains concentrate at large-N transfer, where the priority
features matter most). At N=40 unrolled beats static by +0.31 R²; ~2.9% relative makespan error.

**R² is a harsh metric here** (report MAE/relative too): coupled makespan CV is only 0.07-0.17
(budget compresses the spread), so the ~3-5% relative error of the unrolled model reads as
R²~0.82-0.87. Uncoupled R²=0.997 because its CV is larger and there is no wait fixed-point.

**Next:** swap exact-sim labels for CP-SAT optimal labels to strengthen the amortisation
narrative; add MAE/relative-error columns to the paper's empirical matrix.

## Req 2 — Physics-Fused TAPE (DONE, the model-native explainer) — Modules in `src/ehgat/explain/`
The novel, GNN-centric answer to Req 2: a **faithful-by-construction** explainer built by
transplanting the surrogate's makespan head with a **differentiable Max-Plus DP layer**.
Files (all tests green on pod): `explain/event_dag.py`, `explain/tropical_dp.py`,
`explain/fused_ehgat.py`, `explain/fused_explainer.py`, `explain/train_fused.py`,
`explain/tape_explainer.py` (exact simulator oracle) + `scripts/run_fused_tape.py`,
`tests/unit/test_fused.py` (7) + `tests/unit/test_tape.py` (3).

**Architecture (non-destructive — the scalar `(C_max,E)` head still works):**
- `event_dag.py` is the single shared physics: one expanded max-plus event DAG (per task:
  gate `m(j)`, QC-finish `q(j)`, AGV-free `a(j)`) used by BOTH the exact oracle and the model.
- `tropical_dp.py` is a custom `autograd.Function`: max-plus longest path forward; backward
  routes the subgradient **only along the physical argmax/critical path** → gradients are
  exact binary critical-path indicators (no MLP smearing).
- `fused_ehgat.py` (`FusedEHGATv2`) wraps the **frozen** EHGATv2 core (`core.encode()` exposes
  node embeddings) and adds physics-anchored heads:
  - leg-time head predicts an **O(1) residual around the exact closed-form leg split**
    (empty/loaded legs use independent speed levels, so the split is recovered by discrete
    inversion over the 3×3 power grid — `_leg_time_prior`), piped into the tropical DP for `C_max`.
  - **Energy is strictly exact & additive**: sum of the input arc leg energies (`dE/dleg=1`).
  - node delay = residual around the known handling time.
- `fused_explainer.py`: the model's native gradients ARE the explanation; `faithfulness_report`
  compares the fused critical path to the exact oracle (leg/arc critical Jaccard).
- `train_fused.py`: freezes the core, fits only the heads (anchored leg/`tau` loss +
  `(C_max,E)` MSE), `CosineAnnealingLR` 1e-3→1e-5, logs val R².

**Validated on pod (N=6, `run_fused_tape.py`, `experiments/fused_tape/fused_tape_n6.json`):**
makespan **R²=0.9995** (MAE 1.98 s), energy **R²=1.0000** (MAE 3e-4 kJ — exact by construction),
restoring the ≥0.99 calibration the directive required. Faithfulness vs the exact simulator
TAPE oracle: **leg- and arc-critical Jaccard = 1.00** (the fused model's native critical path
is identical to the exact max-plus critical path — faithful by construction, no smearing).
The point vs Module-6 Sobol: this is **model-native and scalable** — the GNN's own gradients
give per-leg/edge Trade-off Criticality Scores (TCS) in one backward pass.
Run: `python scripts/run_fused_tape.py --tasks 6 10 20` → `experiments/fused_tape/fused_tape_n{N}.json`.

### Tier-1 nonlinear extension — peak-power coupling (the "GNN is load-bearing" ablation)
To make the surrogate genuinely necessary we added a **nonlinear, non-separable** objective: a
fleet-wide instantaneous power budget (`Instance.peak_power`). A deterministic event-driven
simulator (`environment/evaluator.py::_evaluate_power_coupled`) resolves the resulting resource
contention (greedy SGS; exhibits the classic **Graham anomaly**, so makespan is non-monotone in
the budget). The coupled makespan has **no closed form** — it is the longest path over an
activity DAG *plus* power-resolution waits.

Faithful composition WITHOUT discrete arcs: each leg's **effective** max-plus weight is
`leg_time + power_wait`, which lets the precedence-only coupled activity DAG
(`event_dag.py::assemble_coupled_event_dag`) reproduce the coupled makespan **exactly** (proven
in `tests/unit/test_coupled_dag.py`). The GNN therefore predicts a continuous **per-leg power
wait** (`fused_ehgat.py::wait_head`) anchored to the simulator's true waits; the coupled oracle
(`tape_explainer.py::explain_schedule_coupled`) provides the ground-truth coupled critical path.

**Validated on pod (N=8, peak_power=30 kW, `scripts/diag_coupled.py`):**

| model | r2_makespan | r2_energy | leg-critical Jaccard |
|---|---|---|---|
| frozen core **black-box MLP head** | **0.235** | 0.999 | — |
| **fused tropical wait-head** | **0.872** | 1.000 | **1.000** |

Reading: under genuine nonlinear coupling the black-box scalar head **collapses to R²≈0.23**,
while the physics-fused tropical composition lifts makespan to **0.87** and — crucially — gives a
**leg-critical Jaccard of 1.00**, i.e. the model's critical path is *exactly* the coupled
oracle's on every test schedule. **Attribution is faithful-by-construction even when makespan
magnitude is only approximate** (residual C_max MAE ≈ 26 s comes from per-leg wait-magnitude
error, which is hard to learn from a static graph). This is the clean ablation that the GNN +
max-plus layer is load-bearing exactly where the problem stops being separable.

### Scaling study (parallel, `scripts/run_scaling.py`) — the gap WIDENS with N
Runner fans independent `(N, peak_power, seed)` jobs across a CPU process pool (1 BLAS thread
each); also `FusedEHGATv2.encode_cached` caches the **frozen** core embeddings across epochs
(~1.5× faster training, identical R²). 8 jobs (N∈{6,8,10,12} × 2 seeds) finished in ~5 min
wall (vs ~20+ min sequential). Artifact: `experiments/scaling/scaling_pp30.json`.

Per-N means at peak_power=30 kW (black-box core scalar head vs fused tropical head):

| N | core r²_Cmax | fused r²_Cmax | fused r²_E | leg-Jaccard | Cmax MAE |
|---|---|---|---|---|---|
| 6 | 0.523 | 0.868 | 1.000 | 0.875 | 29.7 |
| 8 | 0.175 | 0.867 | 1.000 | 0.978 | 35.8 |
| 10 | **−0.276** | 0.853 | 1.000 | 0.937 | 38.0 |
| 12 | **−0.278** | 0.845 | 1.000 | 0.932 | 52.2 |

Reading: the **black-box MLP head degrades with N and goes negative (worse than the mean) at
N≥10**, while the **physics-fused head holds ~0.85 flat**, energy exact, attribution faithful
(Jaccard 0.87–0.98). The fused−core gap widens with scale (0.34→0.69→1.13→1.12) — exactly the
"GNN + max-plus is load-bearing and *scales*; the black-box collapses" evidence the thesis needs.

Honest scope: Tier-1 eval is still polynomial/cheap, so the surrogate is justified by
generalization/guidance + faithful attribution, not yet by "amortizing an expensive solve".
Closing the makespan-magnitude gap to 0.99 (and making per-candidate eval genuinely expensive)
is the **Tier-2** step: an inner optimal-timing solve under cumulative power (RCPSP/CP-SAT
labels) or stochastic replications. `oracle.py` (exact Pareto front) is **uncoupled-only** — its
speed-DP separability breaks under coupling; the per-schedule simulator is the coupled ground
truth.

## Req 2 — landscape / feature-importance (DONE, headline results) — Module 6
`src/ehgat/benchmark/landscape.py` + `scripts/run_landscape.py` + `tests/unit/test_landscape.py`
(11 tests pass on pod). Computed **on the exact Max-Plus evaluator** (the SCM from decision
variables → `(C_max, E)`), not a surrogate. Artifacts: `experiments/landscape/landscape_n{10,20,50}.json`.

Run: `OMP_NUM_THREADS=1 .venv/bin/python scripts/run_landscape.py --tasks 10 20 50 \
--sobol-base 4096 --cascade-samples 512 --contrast-samples 2048 --shap --shap-samples 3000`

**Findings (stable across N=10/20/50):**
1. **Both objectives are topology-dominated.** Grouped Sobol' total-order: makespan
   ST(sequence)+ST(assignment) ≈ 1.5–1.66 vs speed ≈ 0.05; energy structural ST ≈ 1.34–1.39
   vs speed ≈ 0.12. **Counterintuitive headline:** *energy* is governed by routing
   (empty-leg repositioning distance), NOT the speed knobs — loaded distance is fixed and
   empty_speed barely moves energy (ST≈0.01).
2. **AGVs are the dominant bottleneck:** ~79–84% of exact critical-path mass is AGV-bound
   (2 AGVs vs 3 QCs) at every N. Consistent with Claim 1.
3. **Why Pareto-optimal:** AGV **load balance** is the discriminator — Cliff's δ on
   `agv_load_imbalance` is consistently strongly negative (−0.39 … −0.59; front = balanced).
   Speed descriptors are the weak/secondary trade-off axis.
4. **Claim 3 (TreeSHAP failure boundary), quantified & stable:** exact Sobol' puts
   **0.91–0.97** of importance mass on the topological families; TreeSHAP recovers only
   **0.46–0.56**, underweighting topology by **+0.39 … +0.45** (TV distance ≈ same), spilling
   that mass onto the kinematic speed knobs. This *is* the tabular-flattening failure region.

Core module is Torch/xgboost-free (Sobol+cascade+Pareto pure numpy/scipy); the TreeSHAP
foil (`tabular_failure_boundary`) lazily imports xgboost+shap. Cascade tests need the pod
(critical_path_binding transitively imports Torch); Sobol/Pareto tests run on the Mac too.

## AOS null is REAL, not a harness bug — operator-utility diagnostic (decisive)
`scripts/diagnose_operator_utility.py` measures each operator's Pareto-dominance credit on
the **exact evaluator** (ground truth), and whether utility is conditional on the task's
exact bottleneck type (the oracle's premise). Run N=10/20/50, far-from-front vs near-front
parents. (Pod has only ~1.5 GB RAM — keep `--pool` ≤ ~1000 or the Pareto sort OOM-kills.)

Verdict: **the null is genuine, and the oracle tie is mathematically forced near the front.**
- Operators differ a lot in utility (reassign≈speed ≫ swap_agv ≫ swap_qc); `swap_qc` is
  near-dead (reward≈0, only 30–41% feasible — deadlock rejection). So the harness CAN
  express operator effects (not a dead-pipe bug).
- `utility_gain` (best-op oracle vs random) = +0.18…+0.27 at every N/regime.
- `type_gain` (perfect bottleneck-type oracle vs random): +0.11–0.13 far-from-front but
  **≈0 near the front** (−0.017 / +0.022 / +0.042 at N=10/20/50). Final HV is decided near
  the front → a type-oracle carries ~no usable signal there → **oracle MUST tie random.**
- Mechanism: for AGV-bound near-front tasks the best operator is **`speed`** (≈0.48), not the
  AGV structural ops the oracle picks (reassign 0.25–0.44, swap_agv 0.10–0.28); `reassign` is
  a generalist; `swap_qc` is dead. The type→operator map is simply the wrong map near the
  front. The ablation arms only re-route the low-utility structural ops by type ⇒ no HV move.
- **Takeaway:** the lever is operator *utility*, not bottleneck *type* (utility_gain ≫
  type_gain≈0). Claim 1 (attention faithful to the bottleneck) is untouched — this shows
  faithfulness ≠ usefulness for operator selection. Corrects the earlier note below that
  called reward a clear win: on final HV / IGD+ the reward arm is only **directional**
  (Holm-corrected p=0.12–0.33; the one significant cell is reward>attention GD+ at N=10,
  p≈0.05). Its benefit is convergence-speed (HV-AUC), consistent with utility_gain.

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
7. ~~Req2 landscape module (grouped Sobol on exact evaluator + critical-path attribution).~~
   **DONE** — see the "Req 2 — landscape" section at the top.
8. Surrogate aggregation ablation (max vs mean vs sum).
9. PGExplainer baseline (faithfulness + optimizer arms only).
10. Scaling matrix N ∈ {10,20,50,100}.
11. **GPU parallelization** (the real N=100 lever given 16 vCPU): batched HeteroData
    inference on the L40S (safe — GPU non-determinism affects only the search trajectory,
    not the exact-CPU-evaluator ground-truth metrics); optional batched GPU max-plus
    evaluator (test-validated against the CPU oracle).
12. Reword Claims 1 & 2 to evidence-backed phrasing; assemble tables/figures from JSON.
