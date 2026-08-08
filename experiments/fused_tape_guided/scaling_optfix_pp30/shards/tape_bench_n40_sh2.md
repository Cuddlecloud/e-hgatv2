# Faithful-guidance study -- toy:40 (N=40, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7713 ± 0.0000 | 171.5818 ± 0.0000 | 482.4497 ± 0.0000 | 0.8971 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.5724 ± 0.0000 | 413.1390 ± 0.0000 | 832.2417 ± 0.0000 | 0.9356 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.5185 ± 0.0000 | 327.9859 ± 0.0000 | 1476.0178 ± 0.0000 | 0.8306 ± 0.0000 | 16400 |
| mp-BRKGA | 0.4836 ± 0.0000 | 695.0398 ± 0.0000 | 870.2406 ± 0.0000 | 0.8819 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.3568 ± 0.0000 | 571.9260 ± 0.0000 | 1974.5500 ± 0.0000 | 0.8396 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.633 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.902** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 75.981. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

