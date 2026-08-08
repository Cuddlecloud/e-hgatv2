# Faithful-guidance study -- toy:40 (N=40, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8622 ± 0.0000 | 76.8551 ± 0.0000 | 151.2335 ± 0.0000 | 0.9489 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.9233 ± 0.0000 | 0.0000 ± 0.0000 | 58.8498 ± 0.0000 | 1.0398 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.3685 ± 0.0000 | 673.3655 ± 0.0000 | 997.7596 ± 0.0000 | 0.8241 ± 0.0000 | 32800 |
| mp-BRKGA | 0.6782 ± 0.0000 | 386.1820 ± 0.0000 | 237.6285 ± 0.0000 | 0.7877 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.3923 ± 0.0000 | 667.9350 ± 0.0000 | 1111.7312 ± 0.0000 | 0.7959 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.633 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.902** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 75.981. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

