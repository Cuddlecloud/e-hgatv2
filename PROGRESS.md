# Project Progress & Forward Plan — E-HGATv2 Paper

**Last updated:** 2026-06-27
**Purpose:** Authoritative tracker of what is *established by benchmarks*, what is *ambiguous / needs more runs*, what is *open*, and the prioritized plan to advance rigorously.

---

## 1. SOLID — established by benchmarks, in the paper

| Result | Evidence | Status |
|---|---|---|
| **R2 uncoupled** — variable→objective attribution (AGV speed, crane workload, dispatch order) | `critpath_*_v2.json`: 4 instances (SD-5/8/10, L07), all 8 traversals Jaccard = **1.000**; real speeds/distances/QC IDs in paper | ✅ Solid |
| **TAPE faithfulness (uncoupled)** | `tape_bench_*_unc.json`: leg-Jaccard 0.95–0.98, makespan abs err 11s (toy10) | ✅ Solid |
| **Fidelity study (uncoupled)** | `fused_eval_unc_*`: R²=0.997–0.998, Jaccard=0.98–0.99, 20 seeds, N=6–50 | ✅ Solid |
| **Attention ≠ explanation** | Spearman ρ ≈ 0 (−0.09 to +0.09) across coupled/uncoupled; TAPE ρ high | ✅ Solid, well-supported |
| **R3 optimization vs weak baselines** | `paper_stats.json`: TAPE beats mp-BRKGA, single-pop BRKGA, NSGA-II(random) on HV; Friedman p=8e-6, Holm-corrected | ✅ Solid *vs those baselines* |

---

## 2. AMBIGUOUS / WEAK — claims NOT yet established, need more runs or reframing

### 2.1 ⚠️ R3 headline is statistically weak vs the attention variant
- **Finding:** On HV ratio, `E-HGATv2-TAPE` avg rank = **1.91**, but `E-HGATv2-attn` = **1.45** (attention ranks *better*). TAPE-vs-attn Wilcoxon **p = 0.067 (NOT significant)**, Cliff's δ = −0.21 (small).
- **Implication:** We cannot currently claim "TAPE guidance optimizes better than attention guidance." The defensible claim is narrower: *both GNN-guided variants beat classical baselines; TAPE adds faithful explanation at no optimization cost.*
- **Options:** (a) reframe the claim honestly (recommended, cheap); (b) raise seeds 5→20+ to test if separation emerges; (c) add IGD+/GD+/spread as the primary lens if TAPE wins there. **Decision needed.**

### 2.2 ⚠️ Coupled makespan-extreme critical-path recovery is broken
- **Finding:** `critpath_coupled_toy10_v2.json` makespan-optimal Jaccard = **0.111** (energy-optimal = 1.000). The v2 rerun (unroll=4, 2000 samples) produced **identical** R² (0.898) and Jaccard — **the "fix" did nothing.**
- **Context:** Front-*averaged* coupled fidelity is fine (leg-Jaccard 0.95 toy10 / 0.87 toy20). The failure is specifically at the **makespan extreme**, where all AGVs run at max speed → maximum power contention → hardest DP point.
- **Options:** (a) honestly scope as a stated limitation + report front-averaged Jaccard, not the extreme (recommended baseline); (b) investigate root cause — is it sampling (few training schedules near the makespan extreme), unroll depth, or a genuine surrogate-accuracy ceiling? (c) try targeted sampling weighted toward high-speed schedules. **Decision needed: explain-and-scope vs invest in a fix.**

### 2.3 ✅ R4 (front-behaviour learning) — RESOLVED & REFRAMED (2026-06-27)
- **Original failure:** train corr 0.93 / test corr **−0.49** on a single held-out L07. Root cause was twofold: (a) instance features were hardcoded (num_qcs frozen at 3, num_agvs faked as N/2), and (b) zero structural diversity (all 3 training instances were qc=3). Both fixed in `scripts/run_front_learning.py`.
- **Honest validation:** leave-one-real-out (LORO) across **all 35 real instances** L01–L35 (`scripts/loro_front_learning.py`, `loro_real_results.json`). Train on 34, test on the held-out real instance, repeat.
- **Result — a clean dissociation:**
  - **MAE generalizes (the positive headline):** held-out MAE(transport_frac) **mean 0.048, median 0.047; 97% of instances ≤ 0.08**. The amortized predictor recovers the critical-path composition *magnitude* of unseen real instances WITHOUT running NSGA-II — the "search→knowledge" loop works for composition level.
  - **Per-front ordering does NOT (honest limitation):** median per-instance corr **+0.12** (range −0.95…+0.75); corr ≥ 0.7 in only 3%.
- **Why (mechanism, `front_stability.json`):** **80% of real Pareto fronts are compositionally near-flat** (transport_frac std < 0.06; mean 0.048). Critical-path composition is largely an *instance-structural invariant* — nearly constant along the makespan↔energy trade-off — so there is little within-front ordering signal to recover, and the residual is instance-specific noise the features can't rank.
- **Recommended paper framing:** claim what holds — "predict an unseen instance's critical-path composition from structure alone (MAE ≈ 0.05)" + the structural-invariance finding — and scope the λ-ordering corr as a stated limitation. NOT "predict the λ→composition curve."
- **Note:** synthetic→real transfer is weaker than real→real. Holding out synthetic qc=5 reached corr ≈ 0.55; but a model trained only on synthetic toys fails on real L07 (corr −0.34) even when L07 is bracketed on N/AGV/QC/handling — real instances carry distribution shift. LORO (real→real) is the honest test and is what the above reports.

### 2.4 ⚠️ Uneven seed counts undercut rigor
- Optimization benchmarks (`tape_bench_*`, `paper_stats`): **5 seeds**.
- Fidelity study: **20 seeds**.
- Coupled optimization coverage: only **toy:10, toy:20** (2 instances, 5 seeds each).
- Mismatch invites reviewer pushback. Optimization claims rest on the thinnest sampling.

---

## 3. OPEN PROBLEMS — ranked by value × tractability

| # | Problem | Value | Effort | Recommendation |
|---|---|---|---|---|
| **P1** | R4 generalization (§2.3) | **Highest** — core contribution | ~~Medium~~ | ✅ **DONE** — LORO over 35 real instances; MAE generalizes (0.048), reframed (§2.3) |
| **P2** | R3 claim weak vs attn (§2.1) | High — headline integrity | Low | **Reframe + more seeds** |
| **P3** | Coupled makespan extreme (§2.2) | Medium — honesty/robustness | Low–Med | **Scope as limitation; optional root-cause probe** |
| **P4** | Seed sweep (§2.4) | Medium — reviewer-proofing | Low (compute) | **20+ seeds where it matters** |
| **P5** | Commit fleet-scaling work | Plumbing for P1 | Trivial | **Verify tests, commit** |

---

## 4. FORWARD PLAN

### Phase A — Land the in-flight infrastructure (prereq for P1)
The uncommitted changes (`scripts/run_benchmark.py`, `benchmark/runner.py`, `environment/instance.py`, `tests/unit/test_instance.py`) add `scaled_fleet(N)`, `build_scaling_instance(...)`, and configurable `--agvs/--qcs`. This is exactly the lever P1 needs (vary QC/AGV counts).
- [ ] Run `pytest tests/unit/test_instance.py` and full unit suite — confirm green.
- [ ] Sanity-check `scaled_fleet` policy (AGVs/QCs per N) and `AVAILABLE_QCS` bound (≤ cranes in distance matrix).
- [ ] Commit on a branch.

### Phase B — Fix R4 generalization (P1) — the main scientific work
**Hypothesis:** R4 failed because of zero structural diversity in training (all qc=3). A training set spanning QC counts {2,3,…}, AGV counts, and N should let the predictor learn the *structural* mapping, not memorize 3-crane fronts.
- [ ] Build a diverse instance set with `build_scaling_instance` — vary N, num_qcs ∈ {2,3,4,…}, num_agvs.
- [ ] Regenerate `front_data.json`: NSGA-II front + per-solution TAPE composition per instance.
- [ ] **Leave-one-structure-out evaluation** — hold out a QC count entirely, test generalization to unseen structure (the honest test).
- [ ] Possibly enrich instance features (currently num_tasks/agvs/qcs/handling stats) — but first see if diversity alone fixes corr.
- [ ] **Success criterion:** held-out corr ≳ 0.7 and MAE ≲ 0.08. If it still fails, that is itself a publishable finding (front structure is instance-specific; amortization has limits) — report honestly.
- [ ] Write R4 results section with the leave-one-out table.

### Phase C — Repair the R3 narrative (P2)
- [ ] Rewrite the optimization claim to what the data supports: GNN-guided (both TAPE & attn) > classical baselines; TAPE matches attn on HV **and** adds faithful, exact explanation (the differentiator).
- [ ] Raise optimization seeds 5→20 on at least the core instances; re-run `compute_paper_stats.py`; check whether TAPE/attn separation emerges on any metric.

### Phase D — Coupled honesty pass (P3)
- [ ] In the paper, report coupled **front-averaged** Jaccard (0.95/0.87) as the headline; explicitly state the makespan-extreme degradation (0.11) as a scoped limitation with the power-contention mechanism.
- [ ] *Optional probe:* diagnose whether targeted high-speed-schedule sampling lifts the extreme. Time-box it; do not block the paper.

### Phase E — Seed sweep & finishing (P4)
- [ ] 20+ seeds on scaling + tape_guided; refresh CIs.
- [ ] Recompile paper, verify all pgfplots/TikZ render, table-overflow check.
- [ ] Final proofread.

---

## 5. DECISIONS NEEDED FROM USER (before/while executing)
1. **R3 reframe (§2.1):** accept the honest narrower claim, or invest seeds to chase TAPE>attn significance?
2. **Coupled extreme (§2.2):** scope as a limitation (fast), or invest in a root-cause fix attempt?
3. **R4 scope (§2.3/Phase B):** is "leave-one-QC-count-out generalization" the right bar, or a different held-out axis (N? handling-time regime?)?
4. **Compute budget / VM:** VM is ephemeral — Phase B regeneration + Phase C/E seed sweeps are the compute-heavy steps; sequence them before VM teardown and rsync+commit all artifacts.

---

## 6. DATA LOCATIONS
| Artifact | Path |
|---|---|
| R2 worked examples (v2) | `experiments/critical_path_demo/critpath_*_v2.json` |
| R2 coupled (v1+v2, extreme=0.111) | `experiments/critical_path_demo/critpath_coupled_toy10*.json` |
| R4 front-learning (FAILS generalization) | `experiments/front_learning/front_learning_results.json`, `front_data.json` |
| Optimization benchmark + stats | `experiments/fused_tape_guided/tape_bench_*.json`, `paper_stats.json` |
| Coupled optimization (toy10/20, 5 seeds) | `experiments/fused_tape_guided/tape_bench_toy{10,20}_pp30.json` |
| Fidelity (coupled 20 seeds) | `experiments/fused_eval/fused_eval_coupled_pp30_gnn_predicts_legs.json` |
| Fidelity (uncoupled 20 seeds) | `experiments/fused_eval/fused_eval_unc_c3_gnn_predicts_legs.json` |
| PTS frontier | `experiments/fused_tape_guided/pts_frontier_*.json` |
| Paper source | `paper/main.tex` |
| R4 script | `scripts/run_front_learning.py` |
| Fleet-scaling infra (uncommitted) | `src/ehgat/benchmark/runner.py` (`build_scaling_instance`, `scaled_fleet`) |

---

## 7. VM
```
ssh -p 24520 root@154.42.3.37 -L 8080:localhost:8080   # alias: ehvm
Repo: /workspace/e-hgatv2   Env: uv-managed .venv (torch 2.12.1+cu130)
Hardware: 255 cores, 2× A40 (49 GB). Python 3.12.
```
⚠️ Ephemeral — rsync results to local and commit before teardown.
**Parallelism:** fan independent per-instance jobs across cores with `xargs -P`
(`scripts/run_front_parallel.sh`). GPU does NOT help the front-learning pipeline —
it is CPU-bound on simulator sample generation, not GNN gradient steps.
