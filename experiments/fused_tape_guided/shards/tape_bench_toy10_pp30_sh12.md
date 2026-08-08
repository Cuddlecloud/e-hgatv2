# Faithful-guidance study -- toy:10 (N=10, coupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9055 ± 0.0761 | 38.9132 ± 57.9854 | 49.1193 ± 57.0484 | 1.0667 ± 0.0454 | 8200 |
| E-HGATv2-attn | 0.9025 ± 0.0847 | 41.6637 ± 63.8548 | 49.9489 ± 58.1974 | 1.0049 ± 0.1706 | 8200 |
| NSGA-II (random) | 0.8860 ± 0.0452 | 48.2337 ± 53.8625 | 61.2203 ± 34.6609 | 1.0081 ± 0.1107 | 8200 |
| mp-BRKGA | 0.8065 ± 0.1640 | 81.0242 ± 54.5280 | 120.7271 ± 151.4880 | 1.0157 ± 0.2964 | 8200 |
| single-pop BRKGA | 0.8211 ± 0.0405 | 127.4914 ± 49.4442 | 115.6989 ± 18.4810 | 1.0078 ± 0.1499 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

