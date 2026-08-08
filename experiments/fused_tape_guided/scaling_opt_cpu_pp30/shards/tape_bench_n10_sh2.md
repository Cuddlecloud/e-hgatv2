# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9180 ± 0.0000 | 27.5631 ± 0.0000 | 31.8167 ± 0.0000 | 0.9786 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9721 ± 0.0000 | 7.1947 ± 0.0000 | 9.2678 ± 0.0000 | 0.9149 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.6790 ± 0.0000 | 48.7041 ± 0.0000 | 207.1242 ± 0.0000 | 1.0031 ± 0.0000 | 8200 |
| mp-BRKGA | 0.7026 ± 0.0000 | 120.3562 ± 0.0000 | 121.8952 ± 0.0000 | 0.9488 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.9390 ± 0.0000 | 13.9720 ± 0.0000 | 23.1228 ± 0.0000 | 0.9370 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

