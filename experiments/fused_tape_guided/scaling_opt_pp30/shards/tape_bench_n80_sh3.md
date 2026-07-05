# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8432 ± 0.0000 | 32.7732 ± 0.0000 | 733.4060 ± 0.0000 | 0.8428 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.8230 ± 0.0000 | 70.8607 ± 0.0000 | 665.7327 ± 0.0000 | 0.9286 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.1902 ± 0.0000 | 1630.4145 ± 0.0000 | 4111.1023 ± 0.0000 | 0.9561 ± 0.0000 | 65600 |
| mp-BRKGA | 0.4474 ± 0.0000 | 2462.4632 ± 0.0000 | 1194.0098 ± 0.0000 | 0.6478 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.0961 ± 0.0000 | 2536.5352 ± 0.0000 | 4763.5724 ± 0.0000 | 0.8138 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

