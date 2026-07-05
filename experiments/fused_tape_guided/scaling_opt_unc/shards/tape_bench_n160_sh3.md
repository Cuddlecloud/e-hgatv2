# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7312 ± 0.0000 | 1143.9560 ± 0.0000 | 561.9811 ± 0.0000 | 0.9321 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.5629 ± 0.0000 | 1556.1921 ± 0.0000 | 976.2615 ± 0.0000 | 0.8862 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0048 ± 0.0000 | 6061.1216 ± 0.0000 | 5948.1412 ± 0.0000 | 0.9139 ± 0.0000 | 131200 |
| mp-BRKGA | 0.0000 ± 0.0000 | 6347.7106 ± 0.0000 | 3509.6404 ± 0.0000 | 0.7683 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0000 ± 0.0000 | 5829.6523 ± 0.0000 | 6423.4295 ± 0.0000 | 0.9368 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

