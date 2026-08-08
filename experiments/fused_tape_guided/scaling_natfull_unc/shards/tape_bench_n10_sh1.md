# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9906 ± 0.0000 | 5.0474 ± 0.0000 | 5.1159 ± 0.0000 | 0.8948 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9280 ± 0.0000 | 13.0551 ± 0.0000 | 74.3532 ± 0.0000 | 0.8261 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.8415 ± 0.0000 | 83.3780 ± 0.0000 | 132.8395 ± 0.0000 | 0.8644 ± 0.0000 | 8200 |
| mp-BRKGA | 0.8523 ± 0.0000 | 54.2326 ± 0.0000 | 82.7344 ± 0.0000 | 0.8522 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8781 ± 0.0000 | 42.1990 ± 0.0000 | 85.3265 ± 0.0000 | 0.8695 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

