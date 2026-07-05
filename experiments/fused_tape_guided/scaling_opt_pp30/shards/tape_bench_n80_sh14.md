# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8079 ± 0.0000 | 171.6357 ± 0.0000 | 713.3980 ± 0.0000 | 0.6919 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.7315 ± 0.0000 | 227.1037 ± 0.0000 | 811.2544 ± 0.0000 | 0.7803 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.2111 ± 0.0000 | 1838.0418 ± 0.0000 | 3310.3341 ± 0.0000 | 0.8476 ± 0.0000 | 65600 |
| mp-BRKGA | 0.2160 ± 0.0000 | 2060.3477 ± 0.0000 | 2943.3093 ± 0.0000 | 0.9319 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.1421 ± 0.0000 | 2151.0279 ± 0.0000 | 4530.6130 ± 0.0000 | 0.8242 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

