# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.6953 ± 0.0000 | 168.4561 ± 0.0000 | 1099.0093 ± 0.0000 | 0.9032 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.7311 ± 0.0000 | 359.9341 ± 0.0000 | 892.6597 ± 0.0000 | 0.7614 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.5065 ± 0.0000 | 912.1300 ± 0.0000 | 1787.0115 ± 0.0000 | 0.8343 ± 0.0000 | 65600 |
| mp-BRKGA | 0.9375 ± 0.0000 | 441.0981 ± 0.0000 | 128.6424 ± 0.0000 | 0.9948 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.4405 ± 0.0000 | 787.5324 ± 0.0000 | 2191.6063 ± 0.0000 | 0.8252 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

