# Faithful-guidance study -- toy:40 (N=40, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.6699 ± 0.0000 | 208.6078 ± 0.0000 | 792.2730 ± 0.0000 | 0.9198 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.6368 ± 0.0000 | 19.1389 ± 0.0000 | 1064.3779 ± 0.0000 | 0.9125 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.4461 ± 0.0000 | 533.9472 ± 0.0000 | 1451.6772 ± 0.0000 | 0.9228 ± 0.0000 | 32800 |
| mp-BRKGA | 0.9367 ± 0.0000 | 471.6705 ± 0.0000 | 63.5540 ± 0.0000 | 0.9078 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.4608 ± 0.0000 | 647.2172 ± 0.0000 | 1227.0911 ± 0.0000 | 0.6908 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.633 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.902** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 75.981. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

