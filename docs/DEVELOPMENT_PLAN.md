# E-HGATv2 — Preliminary Codebase Development Plan (DRAFT)

**Goal:** Prove, on a deterministic 10-task toy container-terminal instance, that an
**Explainable Heterogeneous GATv2 (E-HGATv2)** surrogate can guide NSGA-II to the
*exact* Pareto front faster than a stochastic BRKGA baseline — and that its
self-explanation (attention) is a *faithful, useful* bottleneck detector.

This plan operationalizes `SYSTEM_ARCHITECT_DIRECTIVES.md` (Modules 1–5) with
institutional-grade SWE/CI/CD. It is a **draft** intended for iteration.

---

## 0. Method Decision (recorded)

- **Proposed method:** E-HGATv2 — a **heterogeneous**, Max-Plus GATv2 whose attention
  coefficients are the intrinsic, self-explaining bottleneck attribution.
- **Explainer baseline (kept for comparison):** XGBoost surrogate + TreeSHAP, per
  Homayouni & Davari (Paper 3).
- **Supersedes** Directive Module 3's "Homogeneous GATv2Conv" → **Heterogeneous**
  (QC / AGV / LU node types; precedence vs disjunctive-routing edge types).
- **Rationale:** Makespan over a disjunctive schedule graph *is* a max-plus longest
  path; only a max-plus GNN embeds that physics, and edge-level attention is exactly
  the granularity the targeted-mutation operator consumes.

---

## 1. Physical Ground Truth (from Papers 1 & 2)

| Speed level | alpha | Empty | Loaded |
|---|---|---|---|
| Lower  | 0.8 | 4.8 m/s, 7.8 kW  | 2.4 m/s, 11.7 kW |
| Nominal| 1.0 | 6.0 m/s, 10  kW  | 3.0 m/s, 15.0 kW |
| Higher | 1.2 | 7.2 m/s, 13.2 kW | 3.6 m/s, 19.8 kW |

- Travel time scales as `t = distance / v`; energy `E = power * time` per leg.
- QC handling time `tau ~ U(30, 80)` s (seeded → deterministic).
- Distance matrix = Paper 1 Table 4 (asymmetric, unidirectional), stored as data.
- Toy topology: **N=10 tasks, 3 QCs, 2 SA-AGVs**, AGVs start at LU station 1.

---

## 2. Repository Layout (target)

```
E-HGATv2/
├── pyproject.toml              # PEP-621, pinned deps (managed by uv)
├── README.md  LICENSE  .gitignore
├── .pre-commit-config.yaml     # ruff (lint+format), mypy, end-of-file fixers
├── .github/workflows/ci.yml    # lint → typecheck → test+coverage gate
├── noxfile.py                  # reproducible task sessions
├── configs/                    # pydantic-validated YAML
│   ├── environment.yaml  brkga.yaml  gnn.yaml  nsga2.yaml  benchmark.yaml
├── data/
│   └── distance_matrix.json    # Paper 1 Table 4
├── src/ehgat/
│   ├── environment/            # MODULE 1
│   │   ├── physics.py          # speed/energy constants + validators
│   │   ├── distance.py         # load/validate distance matrix
│   │   ├── instance.py         # deterministic 10-task instance builder
│   │   ├── decoder.py          # canonical schedule decoder (shared)
│   │   ├── evaluator.py        # Cmax + E; precedence via Kahn topo-sort
│   │   └── oracle.py           # brute-force exact Pareto front → JSON
│   ├── baselines/
│   │   └── brkga.py            # MODULE 2 — 4N random-key BRKGA
│   ├── surrogate/              # MODULE 3
│   │   ├── graph.py            # schedule → PyG HeteroData (+ semantic asserts)
│   │   ├── ehgatv2.py          # Max-Plus heterogeneous GATv2 + attention hook
│   │   ├── train.py            # offline training (1000 perms, 50 epochs, MSE)
│   │   └── explainer_xgb.py    # XGBoost + TreeSHAP comparison explainer
│   ├── search/                 # MODULE 4
│   │   ├── nsga2.py            # non-dominated sort + crowding distance
│   │   └── attention_mutation.py # max-alpha edge mutation + Kahn cycle check
│   ├── metrics/                # MODULE 5 support
│   │   ├── hypervolume.py  gdplus.py  spread.py
│   └── utils/
│       ├── seeding.py          # global determinism (numpy/torch/random)
│       └── assertions.py       # semantic tensor assertion helpers
├── scripts/run_benchmark.py    # MODULE 5 entrypoint
├── experiments/                # configs + result artifacts (git-ignored heavy)
├── docs/                       # this plan + mkdocs-material site
└── tests/
    ├── unit/  integration/  property/   # property tests via hypothesis
    └── data/golden/                      # frozen Oracle front for regression
```

---

## 3. The Anti–Semantic-Tensor-Error Contract (cross-cutting)

Per Directive §I, every GNN tensor crossing into `torch.cat` / linear projection passes
through `utils/assertions.py`:

- `assert_node_features(x, expected=("Handling_Time","Is_Load","Is_Unload","QC_ID"))`
- `assert_edge_features(e, expected=("Travel_Time","Empty_Energy","Loaded_Energy"))`
- Asserts verify **shape AND semantic index order**; on mismatch raise
  `SemanticTensorError` with a descriptive trace. These run in *all* modes (not
  stripped by `-O`) and are covered by dedicated "must-crash" tests.

---

## 4. Phased Delivery (each phase = PR, green CI, tests-first)

**Phase 0 — Foundations**
- Scaffold, `pyproject.toml`, pre-commit, CI, determinism harness, config loaders.
- DoD: `nox` runs lint+type+test green on an empty package; seeds reproducible.

**Phase 1 — Environment & Oracle (Module 1) — DONE**
- Physics + distance + instance + decoder + evaluator (Kahn) + exact Oracle, all tested.
- `evaluator.py`: timing recurrence as a **max-plus longest path**; Kahn topo-order +
  `ScheduleCycleError` deadlock detection. Hand-computed LOAD/UNLOAD/QC-serialisation/
  speed-tradeoff cases verified.
- `oracle.py`: exact `PF*` = (unique structure enumeration) x (**per-structure speed
  Pareto DP**). The DP removes the `3^(2N)` speed factor by carrying a Pareto set of
  `(makespan, energy, agv_free*, qc_finish*)` states (dominated-state pruning is exact
  by monotonicity; finished resources are zeroed). Arithmetic is **scaled-integer**
  (exact, no float noise) via `_TIME_SCALE=1800`, `_ENERGY_SCALE=720`; `_pareto_min`
  is numpy-vectorised. Cross-validated against a full `3^(2N)` rational brute force.
- **Decision (resolved):** exact instance = `EXACT_TOY_TASKS = 5` (structure space
  grows ~`(N+1)!`; N=5 computes in ~100 s on M1, frozen to
  `tests/data/golden/exact_front_n5.json`: 1248 structures, 91-point front). `N=10`
  remains the scaling instance; an `OracleTooLargeError` guard blocks intractable runs.
- DoD met: `exact_pareto_front` writes the reproducible exact `(Cmax, E)` front; fast
  test validates the golden, slow test recomputes and matches it byte-for-byte.

**Phase 2 — BRKGA Baseline (Module 2) — DONE**
- `search/nsga2.py`: shared NSGA-II primitives (`fast_non_dominated_sort`,
  `crowding_distance`, `order_by_rank_crowding`, `non_dominated_indices`) — decoupled
  from the environment, reused by both BRKGA and the Module-4 search.
- `baselines/brkga.py`: multi-objective BRKGA. Each generation = `Ne` elites (by
  rank/crowding) + `No` biased-uniform-crossover offspring (`inherit_prob=0.7`) + `Nm`
  fresh mutants; decode via the canonical decoder, evaluate `(Cmax, E)`, rank with
  NSGA-II. Maintains an external non-dominated **archive** + per-generation
  `front_history` (for the H1 convergence study). `default_config` => `P=20N`,
  `Ne=0.2P`, `Nm=0.1P`. Deterministic from a single seeded `numpy` Generator.
- Tests: determinism, evaluation count, mutually non-dominated front, chromosome
  validity, `pop_size` guard, and the key **Oracle-bound soundness** (every BRKGA
  point is weakly dominated by golden `PF*`) + extreme/extent recovery on N=5.
- DoD met: BRKGA returns a non-dominated set on the toy; on N=5 (seed 0, 150 gen,
  ~1.7 s) it recovers both extremes exactly and >=50% of `PF*`, all Oracle-bounded.

**Phase 3 — E-HGATv2 Surrogate (Module 3) — DONE**
- `surrogate/graph.py`: a `Schedule` -> typed `HeteroData` builder. One node type
  `task` (`NODE_FEATURES` = Handling_Time, Is_Load, Is_Unload, QC_ID) and two edge types
  mirroring the `{agv_prev->j, qc_prev->j}` precedence arcs: `("task","agv","task")`
  disjunctive resource arcs (carry `EDGE_FEATURES` = Travel_Time, Empty_Energy,
  Loaded_Energy; the AGV-first task gets a self-arc so **summed arc energy == total E**,
  a unit-tested invariant) and `("task","qc","task")` structural serialisation arcs
  (zero features). `assert_graph_semantics` is the violent failsafe (dim + ordered
  signature + index/attr-count), batch-safe.
- `surrogate/ehgatv2.py`: heterogeneous **max-plus GATv2** (`aggr='max'` within each
  resource relation) + **HAN-style semantic attention** across relations. Rationale: a
  *resolved* schedule is a set of chains, so per-relation GATv2 softmax over a single
  predecessor is degenerate (==1); the informative signal is the cross-resource
  `max(agv_ready, qc_ready)` argmax, captured as a learned semantic attention whose
  per-node weight on a relation is exposed as **per-arc criticality** (detached) — the
  bottleneck the Module-4 mutation targets. Dual readout (mean+max node pooling for the
  longest-path makespan; **additive AGV-arc sum** for the additive energy). Feature/
  target standardisation baked in as buffers so RAW physical graphs predict at inference.
- `surrogate/dataset.py` + `train.py`: decode/evaluate random 4N chromosomes -> labelled
  graphs; train/val/test split; 50 epochs MSE on normalised `(Cmax, E)`; held-out R²/MAE.
- `surrogate/explainer_xgb.py`: Torch-free XGBoost baseline on the interpretable 4N
  decision variables (seq position / AGV / empty + loaded speed per task) + TreeSHAP
  attribution (sequencing + speed), Paper-3 style.
- Tests (`learn`-marked): semantic-assert crash tests; attention shape/determinism +
  **non-degeneracy**; held-out accuracy threshold; logged **GNN vs XGBoost** comparison.
- DoD met: on N=5 the GNN reaches **R²≈0.94 (makespan), ≈0.999 (energy)** vs XGBoost
  **≈0.51 / ≈0.44** — the physics-aware encoding wins; reproducible per-arc attention
  matrix; XGBoost+SHAP baseline runs. (Requires `pip install -e ".[learn]"` + `libomp`.)

**Phase 4 — Attention-Guided NSGA-II (Module 4) — DONE**
- `search/attention_nsga2.py`: `(mu + lambda)` NSGA-II over decoded `Schedule`s, reusing
  the `search/nsga2.py` sort/crowding primitives + an external deduplicated archive +
  per-generation `front_history` (mirrors the BRKGA baseline for a fair `P=20N` match).
- **The contribution — attention-guided mutation.** `attention_bottleneck_task` encodes a
  schedule (`surrogate/graph.py`), reads `EHGATv2.attention`, and returns the task
  delivered by the **maximum-attention AGV arc** (the surrogate's learned critical-path
  bottleneck). Mutation is focused on that task via one of three operators: (1) `speed`
  (nudge empty/loaded speed level — trades `Cmax`<->`E`, acyclic); (2) `reassign` (move
  the task to another AGV, re-projecting `global_order` — acyclic by construction);
  (3) `swap` (a **direct** AGV-chain swap with its predecessor that reorders one resource
  chain independently of the QC chains and **can create an AGV/QC deadlock**). Crossover
  is biased-uniform in the canonical random-key space (`encode_canonical`->recombine->
  `decode`, always acyclic).
- **No-deadlock invariant.** Operator (3) is exactly why the evaluator re-validates
  acyclicity: each swap is re-checked with Kahn (`build_precedence`->`ScheduleCycleError`)
  and **rejected on a cycle** (the parent is kept), so every schedule admitted to the
  population is feasible. A real run rejects ~1k cyclic swaps (`deadlocks_rejected`).
- Tests (`learn`-marked): per-operator correctness; **deterministic deadlock case** (swap
  of two same-QC same-AGV tasks returns `None`) + **no-deadlock property test** (60 seeds
  x all tasks); determinism; evaluation accounting; mutually non-dominated front; all
  archive schedules feasible. Slow: **Oracle-bound soundness** (every front point weakly
  dominated by golden `PF*` — robust since objectives use the exact evaluator) and the
  swap-deadlock path is exercised in a full run.
- DoD met: deterministic end-to-end attention-guided run returns an Oracle-bounded
  non-dominated front; Kahn re-validation guarantees the no-deadlock invariant.

**Phase 5 — Benchmark & Effectiveness Proof (Module 5)**
- Charts: (1) Hypervolume vs Generations; (2) Pareto trade-off with BRKGA (red),
  E-HGATv2-NSGA-II (green), Oracle front (solid black).
- Effectiveness experiments (multi-seed, with CIs) below.

---

## 5. Effectiveness Proof Design (why the toy is ideal)

Because the 10-task Oracle yields the **exact** true Pareto front (`PF*`), we can make
*exact* claims rather than relative ones:

- **H1 — Convergence velocity.** E-HGATv2-NSGA-II reaches `PF*` (HV → HV*, GD+ → 0) in
  fewer generations/evaluations than BRKGA. Metric: HV-vs-gen + generations-to-ε.
- **H2 — Guidance is causal.** Attention-guided mutation beats *random* mutation on the
  identical NSGA-II skeleton (ablation isolates the attention contribution).
- **H3 — Attention faithfulness.** Max-`alpha` edges coincide with the *true* critical-path
  bottleneck edges computed exactly from the Oracle (max-plus longest path). Metrics:
  precision@1, Spearman ρ between `alpha` and marginal objective improvement; also
  agreement between `alpha`-ranking and TreeSHAP-ranking.
- **H4 — Surrogate fidelity.** GNN (Cmax, E) prediction error vs XGBoost on held-out set.
- **H5 — Self-explaining vs post-hoc.** E-HGATv2 intrinsic attention matches/beats
  XGBoost+TreeSHAP at bottleneck identification at lower in-loop latency.

Statistics: ≥30 seeds; Mann-Whitney U / bootstrap CIs; report mean ± CI for HV, GD+, Δ.

---

## 6. Tooling & CI/CD

- **Python 3.11**; deps via **uv**; PyTorch + PyTorch Geometric; xgboost + shap;
  numpy/scipy; matplotlib; pytest + hypothesis + pytest-cov; ruff; mypy.
- **pre-commit:** ruff (lint+format), mypy, file hygiene.
- **GitHub Actions:** lint → typecheck → test (coverage gate, e.g. ≥85% on `src/`).
- **Determinism:** centralized `seeding.py`; `torch.use_deterministic_algorithms(True)`;
  every experiment records seed + config hash.
- **Artifacts:** Oracle front + benchmark results versioned under `experiments/`.
- **Docs:** mkdocs-material; this plan as the living architecture doc.

---

## 7. Open Decisions (need your call)

1. **Node/edge typing scope** for the heterogeneous graph (full QC/AGV/LU typing vs a
   lean operation-graph for the preliminary toy).
2. **Keep XGBoost+TreeSHAP baseline** in the preliminary scope (recommended) or defer.
3. **Optimization stack:** implement NSGA-II from scratch (per directive) and use
   `pymoo` only to *validate* hypervolume — confirm acceptable.
4. **Toy instance source:** synthesize from Paper 1 Table 4 / Table 5 sub-sampled to
   N=10, or hand-fix a single canonical instance for fully reproducible demos.
```
