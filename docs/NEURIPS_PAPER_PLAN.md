# E-HGATv2 — NeurIPS Paper Plan & Engineering Reference

## System Context: NeurIPS Target Paper

I am drafting a paper for NeurIPS targeting the intersection of Explainable AI (XAI)
and Neural Combinatorial Optimization (NCO). My architecture uses a frozen, pre-trained
Heterogeneous Graph Attention Network (E-HGATv2) as an evaluative surrogate
(R² ≈ 0.99) inside an NSGA-II loop for a container terminal scheduling problem.

Our **core method** is the GNN's native semantic attention (`w_agv` vs `w_qc`), validated
against a deterministic Max-Plus algebraic oracle (`critical_agv_arcs`). We do **not** use
auxiliary attention-localization losses (to protect the R² ≈ 0.99 surrogate). PGExplainer
is **retained as a post-hoc comparison baseline only** (faithfulness Table 2 + optimizer
ablation Table 3) — *not* the core method and *not* abandoned. [Resolved with user
2026-06-16: compute is unconstrained, so running the PGExplainer comparison is worth it.]

**Role:** Act as co-author and lead engineer. (1) Internalize the three "Breakthrough
Claims" that form the core narrative. (2) Execute the coding directives required to
finalize the empirical proofs and GPU optimizations.

> NOTE (maintainer, resolved 2026-06-16):
> - **PGExplainer scope = comparison baseline** (Option 2). Native-attention AOS is the
>   headline method; PGExplainer is a foil in Tables 2-3; the exact critical path is the
>   oracle upper bound. Build native-attention AOS + oracle ablation FIRST, add the
>   PGExplainer arm after.
> - **Two claims must be reworded to match current evidence** (the doc's own Final Rule):
>   Claim 2 ("we prove attention deterministically guides search") → *hypothesis to test*
>   (attention-guided mutation ≈ random at N=10; the AOS experiment is not yet run);
>   Claim 1 ("forced to learn the exact physical bottlenecks") → *candidate bottleneck
>   explanation* (faithfulness P@1 = 0.617 vs 0.572 random = better-than-chance, not exact).

---

## Part 1: The Three Breakthrough Claims (Paper Narrative)

### Claim 1 — Empirical Resolution of Attention Faithfulness in Physical DAGs
- **Status quo:** The "Attention is Not Explanation" debate is gridlocked in NLP/CV
  because natural language lacks a mathematical ground truth for causality.
- **Breakthrough:** Applying E-HGATv2 to a physically-bounded, Max-Plus constrained
  schedule (a strict DAG) gives a deterministic causal oracle. To achieve R² ≈ 0.99 the
  GNN is pressured to learn the physical bottlenecks; semantic attention weights classify
  the binding constraints without any auxiliary localization loss.

### Claim 2 — XAI-Driven Adaptive Operator Selection (Causally-Guided Evolution)
- **Status quo:** Standard surrogate-assisted EAs treat the surrogate as a black-box
  evaluator while mutation operators are selected at random.
- **Breakthrough:** Close the XAI feedback loop. Extract the semantic attention
  bottleneck classification (`w_agv` vs `w_qc`) aggregated over the parent Pareto front and
  use it to dynamically bias the NSGA-II `_MUTATION_OPS` (AGV-bound → `reassign_agv`;
  QC-bound → `swap_task_order`).

### Claim 3 — Topological Failure Boundary of Tabular Explainers
- **Status quo:** OR relies heavily on tabular XAI (TreeSHAP) for feature importance.
- **Breakthrough:** A "Hybrid Landscape Analysis." Empirically, TreeSHAP captures
  continuous kinematic variables (AGV speed) but structurally fails on cascading
  topological delays (task sequencing). Define the boundary where tabular XAI fails and
  graph-native attention must take over.

---

## Part 2: Engineering Directives

### Directive 1 — AOS Ablation Matrix (proof for Claim 2)
Experimental scaffold to run and log:
- **Random AOS (baseline):** NSGA-II selects operators uniformly at random.
- **Attention AOS (ours):** operator probabilities shifted by E-HGATv2 semantic attention.
- **Oracle AOS (upper bound):** operator probabilities shifted by the exact Max-Plus
  critical path from `faithfulness.py`.
- **Goal:** logs track Hypervolume and generational convergence; show Attention AOS beats
  Random and approaches Oracle.

### Directive 2 — Mandatory GPU Optimizations for the Evaluation Loop
- **PyG HeteroData batching:** collate N offspring graphs into one disjoint `Batch` for
  parallel forward passes (no sequential per-graph inference).
- **Pinned memory & async transfer:** create CPU tensors with `pin_memory=True`, transfer
  via `non_blocking=True` to overlap transfer with exact-solver (Numba) execution.
- **Static graph optimization (optional):** for static batch sizes (e.g. pop=100), wrap
  the frozen `eval()` model in `torch.compile()` or CUDA graphs to cut kernel-launch
  overhead.

---

## The NeurIPS Empirical Matrix (five rigor vectors)

1. **Statistical efficacy (variance test):** run Random/Attention/Oracle AOS over 30
   independent seeds; report HV **and** IGD; Wilcoxon rank-sum (Mann-Whitney U) to show
   Attention-vs-Random gap is significant (p < 0.05).
2. **Scaling-law ablation (complexity stress):** evaluate the three AOS methods across
   N ∈ {10, 20, 50, 100}. Hypothesis: as N grows, Random AOS flatlines while Attention AOS
   holds its convergence trajectory.
3. **Hyperparameter sensitivity (brittleness):** softmax temperature τ on the probability
   shift, sweep τ ∈ {0.1, 0.5, 1.0, 5.0}; map exploitation vs exploration.
4. **Aggregation-window test (signal-to-noise):** aggregate `w_agv`/`w_qc` from (A) entire
   parent population, (B) elite Pareto front only, (C) single best schedule.
5. **Wall-clock compute trade-off (engineering reality):** log wall-clock per generation;
   show attention-extraction cost is negligible vs the generational speedup from pruning
   dead search space.

### Directive 1 (Revised) — NeurIPS Rigor Evaluation Suite
A reproducible, mathematically rigorous pipeline executing five ablation vectors:
1. **Statistical efficacy:** 30 seeds × {Random, Attention, Oracle}; `scipy.stats`
   Wilcoxon rank-sum p-values for HV and IGD at the final generation.
2. **Scaling-law:** parameterized instance loader looping N ∈ {10, 20, 50}; output
   comparative HV curves showing the gap widen with N.
3. **Temperature sensitivity:** τ-parameterized Attention AOS controller; sweep
   τ ∈ {0.1, 0.5, 1.0, 5.0}.
4. **Aggregation window:** config toggle `full_population` / `pareto_front_only` /
   `best_individual`.
5. **Compute profiling:** `torch.profiler` / hi-res timers logging GNN forward overhead vs
   time saved by accelerated convergence.

All outputs logged to structured format (JSON / pandas) for direct matplotlib/seaborn
ingestion.

---

## Core Paper Thesis

E-HGATv2 is not merely a GNN surrogate for combinatorial optimization. It is a physically
grounded, explainable, feedback-driven optimization framework for multi-objective
SA-AGV/QC scheduling. The key contribution: explanations are not only visual or post-hoc;
they are **validated against exact scheduling physics** and **used to guide search**.

---

## Breakthrough Claims To Reinforce

### 1. Physically grounded graph construction
- **Claim:** the schedule is a heterogeneous graph whose nodes/edges map to physical
  mechanisms: tasks, AGV resource arcs, QC precedence arcs, travel time, empty energy,
  loaded energy, handling time.
- **Why:** graph semantics are not arbitrary; edge explanations correspond to real
  operational bottlenecks.
- **Evidence:** exact mapping schedule→tensors; semantic tensor assertions; AGV/QC arcs
  reconstruct evaluator precedence logic.

### 2. Max-plus surrogate matches scheduling physics
- **Claim:** makespan ≈ max-plus longest path over a resolved precedence DAG, so the
  architecture uses **max** aggregation, not generic sum.
- **Why:** architecture is structurally aligned with the objective, not chosen only for
  accuracy.
- **Evidence:** max vs mean/sum aggregation; R²/MAE for makespan and energy; max improves
  bottleneck/critical-path faithfulness.

### 3. Attention can be scientifically tested, not merely asserted
- **Claim:** a rare setting where "attention as explanation" can be validated/refuted with
  exact scheduling physics.
- **Evidence:** precision@1 of top-attention AGV edge vs exact critical AGV arcs; Spearman
  vs marginal speedup; deletion/insertion; vs random; vs PGExplainer and TreeSHAP.
- **Careful wording:** do **not** claim "attention is explanation." Claim: "in this
  physically grounded graph, attention can be evaluated as a candidate bottleneck
  explanation."

### 4. Explanation-guided optimization feedback
- **Claim:** explanations are used as feedback to guide NSGA-II mutation toward bottleneck
  tasks, speeds, AGV assignments, or resource arcs.
- **Evidence (compare):** vanilla NSGA-II, BRKGA, random-guided NSGA-II, attention-guided
  NSGA-II, PGExplainer-guided NSGA-II, hybrid attention+PGExplainer.
- **Metrics:** HV over generations, GD+, spread, exact Pareto coverage, evaluations to
  fixed HV, deadlocks rejected, final archive quality.

### 5. Multi-objective explanation, not single-objective attribution
- **Claim:** explains both makespan and energy trade-offs; can distinguish whether a
  task/edge matters for time, energy, or Pareto structure.
- **Evidence:** objective-specific masks/scores; explanation-disagreement analysis;
  examples where energy-important edges differ from makespan-critical edges; Pareto vs
  dominated comparison.

### 6. Landscape analysis from explanations
- **Claim:** aggregated explanations across schedules → landscape analysis: which task
  positions, AGV assignments, speed decisions, crane workloads, edge types shape outcomes.
- **Why:** satisfies the advisor's second direction.
- **Evidence:** global importance by feature family; task-rank importance; AGV/QC
  bottleneck frequency; speed-level importance; LOAD vs UNLOAD; Pareto vs non-Pareto
  attribution differences.

### 7. Oracle-grounded small-instance science
- **Claim:** for small instances the exact oracle front allows rigorous evaluation of
  surrogate accuracy, search quality, and explanation faithfulness.
- **Evidence:** exact front for N=10; HV gap to oracle; GD+ to oracle; spread; coverage;
  convergence curves.

### 8. Robustness against semantic tensor errors
- **Claim:** the system prevents physically invalid tensor mixing via semantic assertions.
- **Evidence:** tests that corrupt node/edge signatures fail descriptively; no silent
  cross-contamination of travel time, empty/loaded energy, handling time.

---

## GPU / Scaling Optimizations

1. **Batched graph construction** — batched schedule→graph conversion or cache reusable
   node/QC structures (AGV edge attrs vary; node features & static metadata reused).
2. **Batched surrogate inference** — all predictions during search use PyG `Batch`; one
   batched forward per population/candidate pool. Apply to screening, explanation eval,
   PGExplainer training, attention extraction.
3. **Cache static tensors** — node features, QC `edge_index`/`edge_attr`, task metadata,
   distance lookups, loaded distance per task.
4. **Vectorize evaluator where feasible** — vectorize travel/energy; precompute speed-level
   travel/energy tensors per origin-task pair (keep exact Python for correctness baseline).
5. **GPU-native PGExplainer training** — `model.to(device)`, `batch.to(device)`, masks on
   device, no CPU numpy / graph rebuilding in the inner loop.
6. **Mixed precision where safe** — `autocast` for surrogate/PGExplainer training only if
   numerically stable; never for exact oracle/evaluator comparisons.
7. **Avoid CPU-GPU sync** — no `.item()/.numpy()`/detach-to-CPU in hot loops; collect on
   GPU, move only final metrics to CPU.
8. **Population-level candidate screening** — generate k× offspring, predict all in one GPU
   batch, exact-evaluate only the best predicted non-dominated subset ("GPU surrogate
   amortizes expensive exact evaluation").
9. **Explanation caching** — cache explanation scores by canonical schedule hash; reuse on
   repeats.
10. **torch.compile experimentation** — test on EHGATv2 / PGExplainer forward; keep
    optional behind config (PyG support varies).
11. **DataLoader optimization** — larger batches, `pin_memory`, `persistent_workers`,
    pre-generated graph dataset (not per-epoch generation).
12. **Determinism vs speed mode** — deterministic thesis mode (stable seeds) vs throughput
    mode (GPU-optimized, possibly nondeterministic). Report which mode per experiment.

---

## NeurIPS-Ready Experimental Matrix

**A. Surrogate accuracy** — compare E-HGATv2 max vs sum/mean, MLP on flat chromosome,
XGBoost. Metrics: R²/MAE (makespan, energy), inference time.

**B. Explanation faithfulness** — compare attention, PGExplainer, TreeSHAP→task scores,
random. Metrics: critical-path P@1, P@k, Spearman vs marginal speedup, deletion AUC,
insertion AUC, sparsity, stability.

**C. Optimization performance** — compare BRKGA, vanilla NSGA-II, random-guided,
attention-guided, PGExplainer-guided, hybrid. Metrics: HV vs gen, GD+, spread, oracle
coverage, evaluations-to-threshold, wall-clock, final archive size.

**D. Scaling** — N=10 exact oracle; then N=20, 50, 100 (if feasible). For larger N report
runtime, HV proxy, surrogate throughput, exact evaluator calls saved, explanation
stability.

---

## Writing Directives
1. Don't oversell uniqueness ("no one has used GNNs for scheduling"). Better: "the novelty
   is the closed loop — physics-grounded graph surrogate, testable explanation, and
   explanation-guided multi-objective search."
2. Don't say attention is inherently explanation. Say: "we evaluate whether attention
   functions as a faithful bottleneck indicator."
3. Emphasize why the problem is special: exact evaluator + small-instance oracle make
   explanation falsifiable.
4. Keep the advisor's three directions visible: (1) feature engineering via post-hoc
   explanation; (2) landscape analysis of decision variables vs objectives; (3) feedback
   algorithm for optimization.
5. Every claim has a table or figure: architecture diagram, explanation-comparison table,
   critical-path alignment plot, HV convergence plot, Pareto front plot, landscape heatmap,
   GPU throughput table.

---

## Immediate Implementation Priority
1. Implement PGExplainer with tests.
2. Implement explanation evaluation metrics.
3. Add landscape analysis aggregation.
4. Add PGExplainer-guided NSGA-II.
5. Optimize batched graph construction and batched GPU inference.
6. Run ablation matrix.
7. Write paper around validated claims only.

> RESOLVED (Option 2): steps 1 & 4 stay, but PGExplainer is a **comparison baseline**, not
> the headline method. Reorder: build native-attention AOS controller + Oracle/Random/
> Attention ablation FIRST (no new model, reuses existing `w_agv`/`w_qc` + `critical_agv_arcs`),
> then add the PGExplainer arm.

---

## Core Statistical Protocol
- **Experimental unit:** seed-instance pairs (paired). Do **not** treat generations within
  a run as independent samples.
- **Per-run reduction for curves:** (1) final HV, (2) HV AUC over generations,
  (3) evaluations-to-threshold if reached.

### Primary Statistical Tests
1. **Friedman test** — comparing >2 optimizers/explainers across the same seed-instance
   pairs (optimizer set; metrics: final HV, HV AUC, GD+, spread, coverage). If significant:
   Nemenyi post-hoc OR Holm-corrected Wilcoxon (prefer Holm-Wilcoxon for "does ours beat
   each baseline?").
2. **Wilcoxon signed-rank** — paired two-method comparisons (max vs mean, max vs sum,
   attention-guided vs random-guided, PGExplainer-guided vs random-guided, PGExplainer vs
   attention on explanation metrics). Report p, Holm-corrected p, effect size (rank-biserial
   / Cliff's delta), median difference.
3. **Spearman rank correlation** — faithfulness (attention/PGExplainer/TreeSHAP score vs
   marginal makespan speedup). Report mean/median ρ, bootstrap 95% CI, paired Wilcoxon when
   comparing two explainers' ρ.
4. **Bootstrap CIs** — all main metrics (final HV, HV AUC, GD+, P@1, ρ, runtime). Report
   mean ± std, median, 95% CI.
5. **Permutation / McNemar-style paired test for P@1** — key binary metric (top explanation
   hits an exact critical AGV arc): attention vs random, PGExplainer vs random, PGExplainer
   vs attention. If time-limited: paired bootstrap CI + Wilcoxon on per-instance P@1.

### Minimal Required Ablations
- **A1 — Max-plus architecture:** max vs mean vs sum. Metrics: R²/MAE (makespan, energy),
  critical-path P@1. Tests: Friedman across three; Wilcoxon max-vs-mean, max-vs-sum.
- **A2 — Explanation faithfulness:** random, TreeSHAP, attention, PGExplainer. Metrics:
  P@1 vs exact critical arcs, Spearman vs marginal speedup, deletion AUC, sparsity. Tests:
  Friedman across explainers; Holm-Wilcoxon (PGExplainer, attention) vs random.
- **A3 — Optimizer feedback:** BRKGA, vanilla NSGA-II, random-guided, attention-guided,
  PGExplainer-guided. Metrics: final HV, HV AUC, GD+, spread, evaluations-to-threshold.
  Tests: Friedman; Holm-Wilcoxon attention-vs-random, PGExplainer-vs-random,
  PGExplainer-vs-vanilla.
- **A4 — Objective-specific explanation:** makespan vs energy vs both-objective PGExplainer
  masks. Metrics: makespan fidelity, energy fidelity, mask overlap, Spearman vs makespan
  speedup, correlation vs energy perturbation. Tests: Wilcoxon makespan-mask-vs-energy-mask
  on each fidelity.
- **A5 — GPU engineering:** single vs batched inference vs batched+screening vs
  batched+explanation-cache. Metrics: graphs/sec, wall-clock, exact evals saved, HV/sec.
  Tests: bootstrap CIs only.

### Do Not Include (unless extra space)
head-count ablation; hidden-dim ablation; depth ablation (≤1 appendix note); every mutation
operator combo; every tournament/crossover setting; every threshold variant; every
normalization variant; every relation-fusion variant; problem-size scaling beyond N=10 + one
larger N; too many landscape heatmaps.

---

## Minimum Paper Tables
1. **Surrogate ablation** — rows: max / mean / sum / XGBoost(if space). cols: MAE Cmax, MAE
   Energy, R² Cmax, R² Energy, critical-path P@1.
2. **Explanation faithfulness** — rows: random / TreeSHAP / attention / PGExplainer. cols:
   P@1, Spearman ρ, deletion AUC, sparsity, bootstrap CI, corrected p vs random.
3. **Optimizer** — rows: BRKGA / NSGA-II / random-guided / attention-guided /
   PGExplainer-guided. cols: final HV, HV AUC, GD+, spread, evaluations-to-threshold,
   corrected p vs random-guided.
4. **Runtime** — rows: exact only / batched surrogate / surrogate screening / cached
   explanations. cols: graphs/sec, wall-clock, exact evals saved, HV/sec.

## Minimum Figures
1. **HV convergence** — mean curve with 95% CI band.
2. **Pareto front** — oracle, BRKGA, NSGA-II, attention-guided, PGExplainer-guided.
3. **Explanation example** — one schedule: exact critical path, attention scores,
   PGExplainer scores.
4. **Critical-difference / rank plot** — after Friedman (optimizer or explanation).

## Final Rule
Every claim maps to one of four statistical blocks: (1) Friedman + post-hoc for
multi-method; (2) Wilcoxon signed-rank for paired two-method ablations; (3) Spearman +
bootstrap CI for faithfulness; (4) bootstrap CI for robustness/runtime. No redundant
ablations that don't directly support the main claims.
