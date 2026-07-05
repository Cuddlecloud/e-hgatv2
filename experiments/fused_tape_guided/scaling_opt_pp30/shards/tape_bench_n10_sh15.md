# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9221 ± 0.0000 | 35.5621 ± 0.0000 | 23.6028 ± 0.0000 | 1.0505 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9524 ± 0.0000 | 14.0862 ± 0.0000 | 15.0595 ± 0.0000 | 1.0025 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.8399 ± 0.0000 | 70.0652 ± 0.0000 | 62.4038 ± 0.0000 | 0.9057 ± 0.0000 | 8200 |
| mp-BRKGA | 0.5410 ± 0.0000 | 205.6807 ± 0.0000 | 258.1723 ± 0.0000 | 1.0871 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.7008 ± 0.0000 | 243.9864 ± 0.0000 | 142.1546 ± 0.0000 | 1.1111 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

