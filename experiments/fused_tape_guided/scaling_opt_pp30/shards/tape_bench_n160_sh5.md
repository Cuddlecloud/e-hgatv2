# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8849 ± 0.0000 | 207.6044 ± 0.0000 | 534.6955 ± 0.0000 | 0.8646 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.7497 ± 0.0000 | 591.6969 ± 0.0000 | 630.0225 ± 0.0000 | 0.8396 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.2269 ± 0.0000 | 2782.7452 ± 0.0000 | 5062.1356 ± 0.0000 | 0.9874 ± 0.0000 | 131200 |
| mp-BRKGA | 0.2553 ± 0.0000 | 2074.9501 ± 0.0000 | 2939.3993 ± 0.0000 | 0.7699 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.1705 ± 0.0000 | 2338.0614 ± 0.0000 | 5710.3259 ± 0.0000 | 0.7601 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

