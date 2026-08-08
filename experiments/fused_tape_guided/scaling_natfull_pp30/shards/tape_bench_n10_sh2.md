# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9290 ± 0.0000 | 25.0091 ± 0.0000 | 23.4765 ± 0.0000 | 0.9774 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9912 ± 0.0000 | 1.7190 ± 0.0000 | 1.9644 ± 0.0000 | 0.9089 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.6916 ± 0.0000 | 46.3955 ± 0.0000 | 164.7172 ± 0.0000 | 1.0034 ± 0.0000 | 8200 |
| mp-BRKGA | 0.6890 ± 0.0000 | 114.3481 ± 0.0000 | 108.2830 ± 0.0000 | 0.9471 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.9574 ± 0.0000 | 6.3379 ± 0.0000 | 10.1420 ± 0.0000 | 0.9331 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

