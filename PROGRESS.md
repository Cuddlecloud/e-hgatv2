# Project Progress — E-HGATv2 NeurIPS Workshop Paper

**Last updated:** 2026-06-26

---

## COMPLETED

### R2: Landscape Analysis (Feature Importance / Variable-Objective Relationships)
- [x] `scripts/run_critical_path_demo.py` — full worked-example script with AGV assignments, speeds, distances, QC IDs
- [x] Uncoupled runs: SD-5, SD-8, SD-10, L07 — all Jaccard = 1.000 (8/8 traversals)
- [x] Paper section written with real data: per-task speed levels, distances (m), AGV dispatch order, QC workload decomposition
- [x] Three input variables explicitly covered:
  - AGV travelling speed → C_max sensitivity (Eq. speed_sens, with real HIGHER/NOMINAL/LOWER values)
  - Crane workload → per-crane binding time table (QC1: 116s, QC2: 75s, QC3: 70s)
  - Task dispatch order → precedence chain formation (AGV-0: ⟨0,5,4,8,1,7⟩)
- [x] Explains why solutions are Pareto-optimal (speed trade-off: 2.4 vs 3.6 m/s → energy vs makespan)
- [x] Coupled regime paragraph referencing fidelity table (Jaccard 0.91–0.93)
- [x] v2 data in `experiments/critical_path_demo/critpath_*_v2.json`

### R3: Optimization (Feedback Algorithm / Guidance)
- [x] TAPE-guided NSGA-II implementation (`src/ehgat/search/tape_guidance.py`)
- [x] Benchmark on 11 uncoupled instances — TAPE beats mp-BRKGA on all (Friedman p=8e-6)
- [x] Statistical analysis: Wilcoxon, Holm correction, Cliff's delta, bootstrap CIs
- [x] Paper section with HV/IGD+/GD+/Spread results
- [x] Convergence and scaling figures (pgfplots)

### Fidelity Study (20 seeds)
- [x] Uncoupled: R²=0.997–0.998, Jaccard=0.980–0.991 (N=6–50)
- [x] Coupled: R²=0.777–0.805, Jaccard=0.913–0.928 (N=10–50)
- [x] Results in paper Table `tab:fidelity` and Figure `fig:fidelity`

### Paper (`paper/main.tex`)
- [x] Full methodology: graph representation, E-HGATv2, fused architecture, TAPE, guidance algorithm
- [x] Computational notations (ReLU, softmax, readout, GATv2 equations)
- [x] XGBoost/TreeSHAP contrast section
- [x] All figures as inline pgfplots/TikZ (no external PDFs needed)
- [x] Statistical protocol section (Friedman, Nemenyi, Wilcoxon, bootstrap CIs)
- [x] PTS (Pareto Tension Score) section for R4 post-hoc analysis

### Infrastructure
- [x] VM setup (vast.ai, SSH port 22666)
- [x] All experiments reproducible from scripts
- [x] Unit tests passing locally

---

## IN PROGRESS

### Coupled R2 Demo (v2, unroll=4)
- Running on VM: `--unroll 4 --fused-samples 2000 --fused-epochs 100`
- Goal: improve makespan-optimal Jaccard from 0.111 to ~0.9
- First attempt (unroll=2, 1000 samples) got 0.111/1.000 (makespan/energy extremes)

---

## TODO

### R4: Pareto Front Behaviour Learning (HIGH PRIORITY)
**Advisor requirement:** "extract this knowledge in a way the surrogate model learns the Pareto Front behaviour"

**What this means:** Train a model that can *predict* how the critical path (bottleneck structure) shifts across the Pareto front for a *new* instance, without running NSGA-II from scratch. Amortization/generalization benefit.

**Proposed approach:** Front-conditioned fine-tuning with auxiliary head:
1. For each training instance, run NSGA-II → get Pareto set
2. For each Pareto solution, compute TAPE → get critical-path structure
3. Train an auxiliary head: given (instance, λ-weight), predict the critical-set composition
4. Evaluate on held-out instances: can the model predict which variables bind at different front positions without search?

**Status:** Architecture designed, NOT implemented. Needs:
- [ ] Implement auxiliary head in `src/ehgat/surrogate/`
- [ ] Training script (`scripts/run_front_learning.py`)
- [ ] Run on multiple instances (train on SD-5/8/10, test on L07 or vice versa)
- [ ] Evaluation metrics (e.g., predicted vs actual QC% on critical path at λ=0 vs λ=1)
- [ ] Paper section with results

### Coupled Optimization Comparison (R3 extension)
- [ ] Run TAPE-guided NSGA-II on coupled instances (peak-power 30)
- [ ] Compare against mp-BRKGA on same coupled instances
- [ ] Report HV/IGD+ — demonstrates GNN is useful for *optimization* (not just explanation) in coupled regime
- [ ] Add results to paper

### Seed Sweep (statistical robustness)
- [ ] 30 seeds for scaling + tape_guided benchmarks
- [ ] 20 seeds for fused_eval
- [ ] Update paper confidence intervals

### Paper Finishing
- [ ] Add coupled R2 v2 results (when run completes) 
- [ ] Add R4 results section
- [ ] Add coupled optimization section
- [ ] Final proofreading and table overflow checks
- [ ] Compile and verify all figures render

---

## Data Locations

| Artifact | Path |
|---|---|
| R2 uncoupled results (v2) | `experiments/critical_path_demo/critpath_*_v2.json` |
| R2 coupled results | `experiments/critical_path_demo/critpath_coupled_toy10.json` |
| R3 benchmark results | `experiments/fused_tape_guided/` |
| Fidelity study (coupled) | `experiments/fused_eval/fused_eval_coupled_pp30_gnn_predicts_legs.json` |
| Fidelity study (uncoupled) | `experiments/fused_eval/fused_eval_unc_c3_gnn_predicts_legs.json` |
| PTS frontier results | `experiments/fused_tape_guided/pts_frontier_*.json` |
| Paper stats | `experiments/fused_tape_guided/paper_stats.json` |
| Paper source | `paper/main.tex` |

---

## VM Info
```
ssh -p 22666 root@154.42.3.37 -L 8080:localhost:8080
Repo: /workspace/e-hgatv2
Venv: /workspace/venv
```
