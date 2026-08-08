# Faithful-guidance study -- L07 (N=8, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 40x4 = GAT/BRKGA 160/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9394 ± 0.0463 | 5.5255 ± 4.8411 | 34.8470 ± 29.6652 | 0.8319 ± 0.0977 | 6560 |
| E-HGATv2-attn | 0.9411 ± 0.0503 | 7.1748 ± 13.0428 | 33.9343 ± 32.3188 | 0.8412 ± 0.1336 | 6560 |
| NSGA-II (random) | 0.9203 ± 0.0228 | 15.0947 ± 18.9492 | 41.3779 ± 23.1926 | 0.8915 ± 0.1469 | 6560 |
| mp-BRKGA | 0.9141 ± 0.0369 | 25.8941 ± 4.7359 | 41.2743 ± 30.2977 | 0.7699 ± 0.1348 | 6560 |
| single-pop BRKGA | 0.9066 ± 0.0328 | 13.8523 ± 5.0572 | 47.4061 ± 20.9716 | 0.8834 ± 0.0735 | 6560 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.867 | 0.176 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.985** |
| random baseline | 0.125 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 2.221. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

