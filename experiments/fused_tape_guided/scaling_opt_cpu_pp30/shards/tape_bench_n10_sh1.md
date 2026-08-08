# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9327 ± 0.0000 | 20.8053 ± 0.0000 | 31.5657 ± 0.0000 | 1.0798 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9020 ± 0.0000 | 41.4165 ± 0.0000 | 50.5191 ± 0.0000 | 1.0995 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.9258 ± 0.0000 | 41.4019 ± 0.0000 | 62.1517 ± 0.0000 | 1.0102 ± 0.0000 | 8200 |
| mp-BRKGA | 0.8079 ± 0.0000 | 89.1465 ± 0.0000 | 102.2049 ± 0.0000 | 0.8658 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8202 ± 0.0000 | 70.3072 ± 0.0000 | 153.2396 ± 0.0000 | 0.9870 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

