# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8089 ± 0.0000 | 79.5774 ± 0.0000 | 80.2844 ± 0.0000 | 0.9097 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.7663 ± 0.0000 | 73.4244 ± 0.0000 | 96.5966 ± 0.0000 | 1.0880 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.5875 ± 0.0000 | 62.5751 ± 0.0000 | 292.7030 ± 0.0000 | 1.0026 ± 0.0000 | 8200 |
| mp-BRKGA | 0.6740 ± 0.0000 | 138.2101 ± 0.0000 | 134.3241 ± 0.0000 | 0.9555 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8916 ± 0.0000 | 20.7548 ± 0.0000 | 52.9966 ± 0.0000 | 0.9302 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

