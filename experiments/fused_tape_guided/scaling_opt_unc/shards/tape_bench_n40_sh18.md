# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8526 ± 0.0000 | 191.3109 ± 0.0000 | 333.6371 ± 0.0000 | 0.8590 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.9018 ± 0.0000 | 130.2939 ± 0.0000 | 189.6726 ± 0.0000 | 0.8589 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.5756 ± 0.0000 | 809.4364 ± 0.0000 | 1356.5834 ± 0.0000 | 0.9526 ± 0.0000 | 32800 |
| mp-BRKGA | 0.8392 ± 0.0000 | 373.4130 ± 0.0000 | 338.7431 ± 0.0000 | 0.8468 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.6302 ± 0.0000 | 520.7030 ± 0.0000 | 998.5452 ± 0.0000 | 0.7488 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

