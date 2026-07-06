# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8688 ± 0.0000 | 334.4151 ± 0.0000 | 654.6269 ± 0.0000 | 0.8305 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.8777 ± 0.0000 | 348.7299 ± 0.0000 | 380.9959 ± 0.0000 | 0.9232 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.2807 ± 0.0000 | 2364.9246 ± 0.0000 | 4863.6585 ± 0.0000 | 0.9356 ± 0.0000 | 131200 |
| mp-BRKGA | 0.5403 ± 0.0000 | 1931.0057 ± 0.0000 | 1625.9778 ± 0.0000 | 0.6734 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.2519 ± 0.0000 | 2267.9502 ± 0.0000 | 5306.9617 ± 0.0000 | 0.8594 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

