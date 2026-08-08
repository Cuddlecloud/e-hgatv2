# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8859 ± 0.0000 | 37.8051 ± 0.0000 | 33.5487 ± 0.0000 | 0.8834 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9545 ± 0.0000 | 10.3801 ± 0.0000 | 14.5554 ± 0.0000 | 1.1544 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.7414 ± 0.0000 | 202.1698 ± 0.0000 | 74.1126 ± 0.0000 | 0.9536 ± 0.0000 | 8200 |
| mp-BRKGA | 0.8338 ± 0.0000 | 52.9977 ± 0.0000 | 38.7102 ± 0.0000 | 1.0546 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8294 ± 0.0000 | 51.3188 ± 0.0000 | 45.1605 ± 0.0000 | 1.0465 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

