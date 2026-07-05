# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7847 ± 0.0000 | 124.5489 ± 0.0000 | 122.3116 ± 0.0000 | 0.9455 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.8210 ± 0.0000 | 281.0468 ± 0.0000 | 135.4925 ± 0.0000 | 1.1496 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.3476 ± 0.0000 | 552.7670 ± 0.0000 | 518.8766 ± 0.0000 | 0.8259 ± 0.0000 | 16400 |
| mp-BRKGA | 0.6432 ± 0.0000 | 463.6093 ± 0.0000 | 229.2616 ± 0.0000 | 1.0759 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.4369 ± 0.0000 | 429.3467 ± 0.0000 | 410.3034 ± 0.0000 | 0.6224 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

