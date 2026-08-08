# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9765 ± 0.0000 | 7.2832 ± 0.0000 | 5.1244 ± 0.0000 | 0.8704 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.7192 ± 0.0000 | 85.9242 ± 0.0000 | 87.1370 ± 0.0000 | 1.0307 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.5363 ± 0.0000 | 93.1258 ± 0.0000 | 106.0403 ± 0.0000 | 0.7801 ± 0.0000 | 8200 |
| mp-BRKGA | 0.7909 ± 0.0000 | 37.0161 ± 0.0000 | 33.4989 ± 0.0000 | 0.8958 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8948 ± 0.0000 | 11.1096 ± 0.0000 | 16.4770 ± 0.0000 | 0.9327 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

