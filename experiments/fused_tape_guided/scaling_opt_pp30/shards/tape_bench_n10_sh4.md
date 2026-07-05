# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9595 ± 0.0000 | 7.8610 ± 0.0000 | 11.4087 ± 0.0000 | 0.8156 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.8354 ± 0.0000 | 100.2711 ± 0.0000 | 81.9487 ± 0.0000 | 0.9934 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.6474 ± 0.0000 | 231.7370 ± 0.0000 | 154.4747 ± 0.0000 | 0.9527 ± 0.0000 | 8200 |
| mp-BRKGA | 0.7280 ± 0.0000 | 123.0343 ± 0.0000 | 133.1049 ± 0.0000 | 1.0560 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.7202 ± 0.0000 | 120.8493 ± 0.0000 | 111.4397 ± 0.0000 | 1.0480 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

