# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.6962 ± 0.0000 | 1591.4075 ± 0.0000 | 835.8412 ± 0.0000 | 1.0776 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.7219 ± 0.0000 | 821.9990 ± 0.0000 | 632.9610 ± 0.0000 | 0.8322 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.1075 ± 0.0000 | 2966.9677 ± 0.0000 | 4070.8972 ± 0.0000 | 0.9056 ± 0.0000 | 65600 |
| mp-BRKGA | 0.3976 ± 0.0000 | 3549.9604 ± 0.0000 | 1055.4658 ± 0.0000 | 0.8085 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.0491 ± 0.0000 | 2791.1383 ± 0.0000 | 5041.7073 ± 0.0000 | 0.8897 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

