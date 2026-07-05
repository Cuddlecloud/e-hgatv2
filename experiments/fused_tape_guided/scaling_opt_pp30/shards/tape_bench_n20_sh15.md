# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7619 ± 0.0000 | 130.6525 ± 0.0000 | 211.4841 ± 0.0000 | 0.9428 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.8897 ± 0.0000 | 85.8828 ± 0.0000 | 70.1009 ± 0.0000 | 1.0846 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.5579 ± 0.0000 | 246.5368 ± 0.0000 | 480.4887 ± 0.0000 | 0.7372 ± 0.0000 | 16400 |
| mp-BRKGA | 0.5817 ± 0.0000 | 505.2606 ± 0.0000 | 338.6867 ± 0.0000 | 1.0481 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.6621 ± 0.0000 | 335.1043 ± 0.0000 | 238.8494 ± 0.0000 | 0.9827 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

