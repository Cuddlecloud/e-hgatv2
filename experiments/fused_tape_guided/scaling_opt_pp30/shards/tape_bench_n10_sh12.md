# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8983 ± 0.0000 | 66.4911 ± 0.0000 | 58.0998 ± 0.0000 | 1.1083 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.8279 ± 0.0000 | 92.7117 ± 0.0000 | 86.8332 ± 0.0000 | 0.8791 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.7757 ± 0.0000 | 126.8724 ± 0.0000 | 97.6754 ± 0.0000 | 1.0688 ± 0.0000 | 8200 |
| mp-BRKGA | 0.7271 ± 0.0000 | 181.0519 ± 0.0000 | 115.5252 ± 0.0000 | 0.8117 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.6998 ± 0.0000 | 230.3452 ± 0.0000 | 138.8993 ± 0.0000 | 1.0197 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

