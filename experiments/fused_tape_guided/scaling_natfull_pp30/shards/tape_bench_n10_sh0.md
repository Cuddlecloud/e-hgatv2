# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9830 ± 0.0000 | 0.0000 ± 0.0000 | 23.6622 ± 0.0000 | 1.0207 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9339 ± 0.0000 | 31.4784 ± 0.0000 | 45.3671 ± 0.0000 | 1.1473 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.8689 ± 0.0000 | 65.7427 ± 0.0000 | 92.5549 ± 0.0000 | 0.9235 ± 0.0000 | 8200 |
| mp-BRKGA | 0.8184 ± 0.0000 | 64.7898 ± 0.0000 | 126.6873 ± 0.0000 | 1.0546 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8092 ± 0.0000 | 82.4809 ± 0.0000 | 217.8893 ± 0.0000 | 0.8859 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

