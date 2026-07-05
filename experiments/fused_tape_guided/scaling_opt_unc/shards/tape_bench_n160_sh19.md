# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.4285 ± 0.0000 | 2624.6218 ± 0.0000 | 1754.3353 ± 0.0000 | 0.9216 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.5179 ± 0.0000 | 1155.6940 ± 0.0000 | 1447.7952 ± 0.0000 | 0.7246 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0000 ± 0.0000 | 5490.7832 ± 0.0000 | 6418.6279 ± 0.0000 | 0.9627 ± 0.0000 | 131200 |
| mp-BRKGA | 0.0045 ± 0.0000 | 4619.8727 ± 0.0000 | 2487.6023 ± 0.0000 | 0.7254 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0000 ± 0.0000 | 6114.4996 ± 0.0000 | 6847.3634 ± 0.0000 | 0.8661 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

