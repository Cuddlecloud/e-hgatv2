# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.6460 ± 0.0000 | 137.9397 ± 0.0000 | 227.0064 ± 0.0000 | 0.9008 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.7997 ± 0.0000 | 76.0579 ± 0.0000 | 84.1272 ± 0.0000 | 1.0376 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.8837 ± 0.0000 | 32.2187 ± 0.0000 | 47.6322 ± 0.0000 | 0.7885 ± 0.0000 | 8200 |
| mp-BRKGA | 0.6764 ± 0.0000 | 177.6589 ± 0.0000 | 155.2574 ± 0.0000 | 1.1236 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.7098 ± 0.0000 | 113.7149 ± 0.0000 | 135.6330 ± 0.0000 | 0.8038 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

