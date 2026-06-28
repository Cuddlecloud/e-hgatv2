# Faithful-guidance study -- toy:10 (N=10, coupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 1.0078 ± 0.1764 | 30.9698 ± 25.1634 | 12.0518 ± 11.5097 | 1.0751 ± 0.0358 | 8200 |
| E-HGATv2-attn | 1.1448 ± 0.1093 | 1.1103 ± 3.5107 | 3.9051 ± 4.9493 | 0.8782 ± 0.1165 | 8200 |
| NSGA-II (random) | 1.0246 ± 0.2033 | 60.2528 ± 152.5516 | 12.9294 ± 15.8773 | 1.0068 ± 0.0987 | 8200 |
| mp-BRKGA | 0.8626 ± 0.2840 | 104.6930 ± 112.0694 | 52.5306 ± 86.3731 | 1.0133 ± 0.2338 | 8200 |
| single-pop BRKGA | 0.9026 ± 0.1430 | 63.7083 ± 129.5807 | 41.8124 ± 16.9452 | 1.0545 ± 0.1386 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

