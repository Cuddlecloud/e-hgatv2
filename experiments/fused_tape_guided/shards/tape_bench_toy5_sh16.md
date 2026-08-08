# Faithful-guidance study -- toy:5 (N=5, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 25x4 = GAT/BRKGA 100/gen). Reference: exact Oracle. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9697 ± 0.0478 | 0.8848 ± 0.4161 | 21.3143 ± 36.7675 | 0.9357 ± 0.0849 | 4100 |
| E-HGATv2-attn | 0.9822 ± 0.0038 | 1.5429 ± 0.5799 | 4.5126 ± 1.0221 | 0.9865 ± 0.0522 | 4100 |
| NSGA-II (random) | 0.9637 ± 0.0412 | 2.5191 ± 2.3645 | 24.0040 ± 36.0134 | 0.9450 ± 0.1474 | 4100 |
| mp-BRKGA | 0.9318 ± 0.0291 | 42.2439 ± 67.1540 | 29.3782 ± 27.5696 | 0.8848 ± 0.0521 | 4100 |
| single-pop BRKGA | 0.9702 ± 0.0461 | 5.1683 ± 9.7869 | 15.6446 ± 35.1406 | 0.9747 ± 0.1689 | 4100 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.062 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.980** |
| random baseline | 0.200 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 8.114. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

