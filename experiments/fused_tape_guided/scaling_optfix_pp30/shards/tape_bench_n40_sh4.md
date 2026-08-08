# Faithful-guidance study -- toy:40 (N=40, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7180 ± 0.0000 | 261.9303 ± 0.0000 | 631.8347 ± 0.0000 | 0.8980 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7281 ± 0.0000 | 175.0248 ± 0.0000 | 689.3504 ± 0.0000 | 0.9761 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.4660 ± 0.0000 | 432.7164 ± 0.0000 | 1397.8656 ± 0.0000 | 0.9997 ± 0.0000 | 16400 |
| mp-BRKGA | 0.5386 ± 0.0000 | 832.4504 ± 0.0000 | 546.5288 ± 0.0000 | 0.9460 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.3626 ± 0.0000 | 659.3832 ± 0.0000 | 1842.6528 ± 0.0000 | 0.8720 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.633 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.902** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 75.981. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

