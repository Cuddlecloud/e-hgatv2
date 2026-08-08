# Faithful-guidance study -- toy:40 (N=40, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7185 ± 0.0000 | 189.3813 ± 0.0000 | 763.7251 ± 0.0000 | 0.9227 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.9476 ± 0.0000 | 45.8418 ± 0.0000 | 91.3712 ± 0.0000 | 0.8959 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.3514 ± 0.0000 | 717.3895 ± 0.0000 | 1323.4822 ± 0.0000 | 0.9907 ± 0.0000 | 32800 |
| mp-BRKGA | 0.7332 ± 0.0000 | 232.1213 ± 0.0000 | 229.7263 ± 0.0000 | 0.7441 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.4312 ± 0.0000 | 591.7068 ± 0.0000 | 1196.2968 ± 0.0000 | 0.7231 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.633 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.902** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 75.981. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

