# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8328 ± 0.0000 | 502.3089 ± 0.0000 | 1094.1307 ± 0.0000 | 1.0324 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.9036 ± 0.0000 | 290.8668 ± 0.0000 | 325.0015 ± 0.0000 | 0.7807 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.2582 ± 0.0000 | 2353.4622 ± 0.0000 | 5638.3569 ± 0.0000 | 0.8966 ± 0.0000 | 131200 |
| mp-BRKGA | 0.5611 ± 0.0000 | 1257.9109 ± 0.0000 | 1331.1113 ± 0.0000 | 0.9777 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.2382 ± 0.0000 | 2413.4362 ± 0.0000 | 5766.6191 ± 0.0000 | 0.8473 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

