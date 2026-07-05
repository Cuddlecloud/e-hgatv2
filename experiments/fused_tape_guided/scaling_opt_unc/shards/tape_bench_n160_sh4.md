# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.3889 ± 0.0000 | 1695.6695 ± 0.0000 | 1849.2980 ± 0.0000 | 0.8970 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.5983 ± 0.0000 | 1204.5749 ± 0.0000 | 1020.1345 ± 0.0000 | 0.8358 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0007 ± 0.0000 | 4256.8559 ± 0.0000 | 5687.8706 ± 0.0000 | 0.9348 ± 0.0000 | 131200 |
| mp-BRKGA | 0.0000 ± 0.0000 | 5457.1714 ± 0.0000 | 4124.5337 ± 0.0000 | 0.8695 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0000 ± 0.0000 | 5747.4786 ± 0.0000 | 6813.3662 ± 0.0000 | 0.8247 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

