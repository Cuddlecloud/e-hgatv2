# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9144 ± 0.0000 | 26.6978 ± 0.0000 | 26.8440 ± 0.0000 | 0.9993 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9460 ± 0.0000 | 14.3380 ± 0.0000 | 17.2332 ± 0.0000 | 1.0899 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.8940 ± 0.0000 | 50.7591 ± 0.0000 | 33.5455 ± 0.0000 | 1.0268 ± 0.0000 | 8200 |
| mp-BRKGA | 0.7744 ± 0.0000 | 68.1689 ± 0.0000 | 74.5157 ± 0.0000 | 0.9856 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.7159 ± 0.0000 | 110.3500 ± 0.0000 | 119.9953 ± 0.0000 | 0.9145 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

