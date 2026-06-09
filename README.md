# E-HGATv2

**Explainable Heterogeneous GATv2-guided NSGA-II** for energy-efficient scheduling of
speed-adjustable AGVs (SA-AGVs) and quay cranes (QCs) in a dual-cycling container terminal.

This repository delivers a preliminary, fully-reproducible **10-task toy demonstration**
that the attention of a self-explaining Max-Plus heterogeneous GATv2 surrogate can guide
NSGA-II to the *exact* Pareto front faster than a stochastic BRKGA baseline — and that the
attention is a faithful, useful bottleneck detector.

See [`docs/DEVELOPMENT_PLAN.md`](docs/DEVELOPMENT_PLAN.md) for the architecture, phased plan,
and effectiveness-proof design, and [`SYSTEM_ARCHITECT_DIRECTIVES.md`](SYSTEM_ARCHITECT_DIRECTIVES.md)
for the governing directives.

## Scientific grounding

| Paper | Role |
|---|---|
| Homayouni & Fontes (2022) | Base MILP physics, distance matrix, dual-cycling |
| Fontes & Homayouni (2022) | Improved single-index MILP, mp-BRKGA, GD+/Spread, PF* construction |
| Homayouni & Davari | XAI-guided NSGA-II concept (here realized via E-HGATv2 attention) |

## Quickstart

```bash
# Create the project environment (Python 3.12) and install core deps
uv sync --python 3.12

# Phase 1+2 (environment, oracle, BRKGA) need no heavy ML deps.
uv run pytest -m "not learn"

# Add the learning + viz stacks when working on the surrogate / benchmarks
uv sync --python 3.12 --extra learn --extra viz
```

## Layout

```
src/ehgat/
  environment/   # Module 1: physics, distances, instance, decoder, evaluator, oracle
  baselines/     # Module 2: BRKGA
  surrogate/     # Module 3: E-HGATv2 + XGBoost/TreeSHAP explainer baseline
  search/        # Module 4: NSGA-II + attention-guided mutation
  metrics/       # hypervolume, GD+, spread
  utils/         # determinism, semantic-tensor assertions
```

## Reproducibility

All randomness is centrally seeded (`ehgat.utils.seeding`). The GNN runs on **CPU** for
deterministic `scatter`/`max` aggregation. Every experiment records its seed and config hash.
