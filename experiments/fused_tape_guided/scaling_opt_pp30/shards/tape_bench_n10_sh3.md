# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8471 ± 0.0000 | 58.4283 ± 0.0000 | 58.4902 ± 0.0000 | 0.9965 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.7647 ± 0.0000 | 61.0899 ± 0.0000 | 89.1351 ± 0.0000 | 1.1684 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.5966 ± 0.0000 | 279.1302 ± 0.0000 | 222.6920 ± 0.0000 | 1.0640 ± 0.0000 | 8200 |
| mp-BRKGA | 0.8345 ± 0.0000 | 399.2183 ± 0.0000 | 48.2269 ± 0.0000 | 1.0929 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.7136 ± 0.0000 | 260.5068 ± 0.0000 | 104.5197 ± 0.0000 | 0.8472 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

