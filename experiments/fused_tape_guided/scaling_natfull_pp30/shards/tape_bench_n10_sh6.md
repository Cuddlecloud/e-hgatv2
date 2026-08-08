# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9458 ± 0.0000 | 3.3640 ± 0.0000 | 9.7267 ± 0.0000 | 0.9934 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9527 ± 0.0000 | 5.2893 ± 0.0000 | 9.1199 ± 0.0000 | 0.9120 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.8929 ± 0.0000 | 121.1210 ± 0.0000 | 44.7406 ± 0.0000 | 1.0545 ± 0.0000 | 8200 |
| mp-BRKGA | 0.6197 ± 0.0000 | 352.1000 ± 0.0000 | 151.9082 ± 0.0000 | 0.9750 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8219 ± 0.0000 | 151.8592 ± 0.0000 | 83.6923 ± 0.0000 | 0.8972 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

