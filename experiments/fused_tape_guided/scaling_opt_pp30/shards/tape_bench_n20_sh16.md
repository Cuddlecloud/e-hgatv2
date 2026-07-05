# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8607 ± 0.0000 | 55.2055 ± 0.0000 | 54.4678 ± 0.0000 | 0.8957 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7531 ± 0.0000 | 266.7368 ± 0.0000 | 88.6196 ± 0.0000 | 1.1641 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.4760 ± 0.0000 | 299.8070 ± 0.0000 | 274.9518 ± 0.0000 | 0.8212 ± 0.0000 | 16400 |
| mp-BRKGA | 0.4083 ± 0.0000 | 502.9518 ± 0.0000 | 288.5726 ± 0.0000 | 1.1940 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.6067 ± 0.0000 | 134.2075 ± 0.0000 | 287.7502 ± 0.0000 | 0.9258 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

