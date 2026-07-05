# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8574 ± 0.0000 | 11.0203 ± 0.0000 | 703.2012 ± 0.0000 | 0.8873 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.7105 ± 0.0000 | 243.9966 ± 0.0000 | 1005.7635 ± 0.0000 | 0.8019 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.1091 ± 0.0000 | 1956.2272 ± 0.0000 | 4292.2602 ± 0.0000 | 0.7817 ± 0.0000 | 65600 |
| mp-BRKGA | 0.1973 ± 0.0000 | 1720.1564 ± 0.0000 | 2496.2112 ± 0.0000 | 0.9184 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.1157 ± 0.0000 | 2343.5179 ± 0.0000 | 4085.0944 ± 0.0000 | 0.9073 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

