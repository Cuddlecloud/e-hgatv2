# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8291 ± 0.0000 | 108.9976 ± 0.0000 | 359.2827 ± 0.0000 | 1.1438 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.9450 ± 0.0000 | 6.5139 ± 0.0000 | 69.5773 ± 0.0000 | 0.9115 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.8577 ± 0.0000 | 19.7451 ± 0.0000 | 236.0474 ± 0.0000 | 0.8658 ± 0.0000 | 16400 |
| mp-BRKGA | 0.8018 ± 0.0000 | 237.7156 ± 0.0000 | 246.9836 ± 0.0000 | 0.9397 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.8203 ± 0.0000 | 135.6915 ± 0.0000 | 268.5855 ± 0.0000 | 0.7356 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

