# Faithful-guidance study -- toy:5 (N=5, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 25x4 = GAT/BRKGA 100/gen). Reference: exact Oracle. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9707 ± 0.0436 | 1.2459 ± 1.2201 | 21.8409 ± 37.5145 | 0.9125 ± 0.0728 | 4100 |
| E-HGATv2-attn | 0.9832 ± 0.0017 | 1.0535 ± 0.4538 | 4.1735 ± 0.5448 | 0.9655 ± 0.0584 | 4100 |
| NSGA-II (random) | 0.9737 ± 0.0321 | 1.9149 ± 1.3625 | 14.0953 ± 29.1696 | 0.9676 ± 0.1391 | 4100 |
| mp-BRKGA | 0.9318 ± 0.0291 | 42.2439 ± 67.1540 | 29.3782 ± 27.5696 | 0.8848 ± 0.0521 | 4100 |
| single-pop BRKGA | 0.9701 ± 0.0430 | 1.8668 ± 0.7077 | 15.4702 ± 34.2351 | 0.9085 ± 0.0987 | 4100 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.062 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.980** |
| random baseline | 0.200 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 8.114. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

