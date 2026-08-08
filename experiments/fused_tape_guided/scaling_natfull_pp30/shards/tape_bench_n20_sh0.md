# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7335 ± 0.0000 | 132.9476 ± 0.0000 | 204.1852 ± 0.0000 | 0.8942 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.9998 ± 0.0000 | 0.1075 ± 0.0000 | 0.6421 ± 0.0000 | 0.9393 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.4808 ± 0.0000 | 451.2134 ± 0.0000 | 576.8847 ± 0.0000 | 0.7210 ± 0.0000 | 16400 |
| mp-BRKGA | 0.5230 ± 0.0000 | 637.5849 ± 0.0000 | 186.7617 ± 0.0000 | 1.0438 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.7221 ± 0.0000 | 94.6580 ± 0.0000 | 134.2595 ± 0.0000 | 1.0707 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

