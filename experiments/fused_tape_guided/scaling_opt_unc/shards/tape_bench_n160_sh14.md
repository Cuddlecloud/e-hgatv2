# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9524 ± 0.0000 | 0.0000 ± 0.0000 | 75.6542 ± 0.0000 | 0.7574 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.5381 ± 0.0000 | 1802.6819 ± 0.0000 | 1089.5817 ± 0.0000 | 0.8672 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0000 ± 0.0000 | 6883.4984 ± 0.0000 | 5922.5587 ± 0.0000 | 1.0319 ± 0.0000 | 131200 |
| mp-BRKGA | 0.0012 ± 0.0000 | 6605.7191 ± 0.0000 | 5222.2331 ± 0.0000 | 0.8379 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0000 ± 0.0000 | 5983.7121 ± 0.0000 | 6440.6712 ± 0.0000 | 0.8946 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

