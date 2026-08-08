# Faithful-guidance study -- toy:15 (N=15, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 75x4 = GAT/BRKGA 300/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8694 ± 0.0703 | 86.6490 ± 42.1289 | 118.8164 ± 95.2698 | 0.9222 ± 0.1123 | 12300 |
| E-HGATv2-attn | 0.8436 ± 0.0525 | 101.8642 ± 49.3670 | 126.6475 ± 41.5623 | 0.9438 ± 0.1194 | 12300 |
| NSGA-II (random) | 0.8227 ± 0.0465 | 120.5539 ± 37.0346 | 150.7625 ± 64.5534 | 0.8947 ± 0.1074 | 12300 |
| mp-BRKGA | 0.7860 ± 0.1365 | 164.0057 ± 174.1005 | 200.3176 ± 147.4218 | 0.9608 ± 0.1456 | 12300 |
| single-pop BRKGA | 0.8294 ± 0.0413 | 94.4593 ± 42.8857 | 137.2099 ± 77.4425 | 0.8432 ± 0.0480 | 12300 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.800 | 0.081 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.067 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.749. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

