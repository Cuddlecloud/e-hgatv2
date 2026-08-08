# Faithful-guidance study -- toy:40 (N=40, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8431 ± 0.0000 | 72.0439 ± 0.0000 | 376.5936 ± 0.0000 | 0.9821 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.5414 ± 0.0000 | 419.1914 ± 0.0000 | 943.6415 ± 0.0000 | 0.7818 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.4461 ± 0.0000 | 561.4049 ± 0.0000 | 908.9913 ± 0.0000 | 0.6254 ± 0.0000 | 16400 |
| mp-BRKGA | 0.6318 ± 0.0000 | 550.3129 ± 0.0000 | 469.5509 ± 0.0000 | 0.9718 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.3049 ± 0.0000 | 794.5465 ± 0.0000 | 1919.6726 ± 0.0000 | 0.9107 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.633 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.902** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 75.981. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

