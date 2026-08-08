# Faithful-guidance study -- toy:20 (N=20, coupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7791 ± 0.0566 | 96.7805 ± 35.7739 | 348.3148 ± 76.5523 | 0.9290 ± 0.1235 | 16400 |
| E-HGATv2-attn | 0.7802 ± 0.1127 | 136.3588 ± 128.7702 | 164.5847 ± 148.0685 | 0.9978 ± 0.1744 | 16400 |
| NSGA-II (random) | 0.6344 ± 0.2051 | 178.8772 ± 110.8744 | 511.9667 ± 201.8891 | 0.8337 ± 0.1045 | 16400 |
| mp-BRKGA | 0.6074 ± 0.0889 | 357.2659 ± 108.9605 | 297.6170 ± 132.1300 | 1.1349 ± 0.1405 | 16400 |
| single-pop BRKGA | 0.6427 ± 0.1451 | 211.9772 ± 154.6407 | 491.3386 ± 60.9026 | 0.8361 ± 0.2627 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

