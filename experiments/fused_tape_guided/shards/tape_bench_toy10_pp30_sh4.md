# Faithful-guidance study -- toy:10 (N=10, coupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8470 ± 0.1274 | 66.1873 ± 103.8294 | 58.0264 ± 49.4796 | 0.9476 ± 0.1095 | 8200 |
| E-HGATv2-attn | 0.8445 ± 0.1707 | 51.4309 ± 71.0147 | 62.2325 ± 83.9933 | 0.9996 ± 0.1836 | 8200 |
| NSGA-II (random) | 0.7110 ± 0.1396 | 192.8594 ± 154.1296 | 112.9148 ± 62.4613 | 0.9226 ± 0.1758 | 8200 |
| mp-BRKGA | 0.6914 ± 0.1661 | 190.6041 ± 216.4795 | 123.7549 ± 78.1130 | 1.0037 ± 0.1175 | 8200 |
| single-pop BRKGA | 0.7919 ± 0.1398 | 91.9277 ± 91.4349 | 79.0068 ± 52.6004 | 0.9577 ± 0.1012 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

