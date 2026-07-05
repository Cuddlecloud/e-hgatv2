# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.5620 ± 0.0000 | 1128.9789 ± 0.0000 | 1216.9544 ± 0.0000 | 0.7482 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.8730 ± 0.0000 | 312.8316 ± 0.0000 | 236.6166 ± 0.0000 | 0.6505 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0000 ± 0.0000 | 3997.1846 ± 0.0000 | 6246.1967 ± 0.0000 | 0.9524 ± 0.0000 | 131200 |
| mp-BRKGA | 0.0000 ± 0.0000 | 6636.3381 ± 0.0000 | 4688.5644 ± 0.0000 | 0.8667 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0000 ± 0.0000 | 5219.8530 ± 0.0000 | 7075.1850 ± 0.0000 | 0.8631 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

