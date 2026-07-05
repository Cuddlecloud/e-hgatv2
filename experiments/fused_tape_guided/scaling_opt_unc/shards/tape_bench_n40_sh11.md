# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8920 ± 0.0000 | 203.7525 ± 0.0000 | 439.9274 ± 0.0000 | 0.9392 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.9267 ± 0.0000 | 114.3701 ± 0.0000 | 158.0124 ± 0.0000 | 0.9989 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.6404 ± 0.0000 | 520.0144 ± 0.0000 | 1393.0075 ± 0.0000 | 0.6914 ± 0.0000 | 32800 |
| mp-BRKGA | 0.8269 ± 0.0000 | 348.9065 ± 0.0000 | 516.3149 ± 0.0000 | 0.9617 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.5866 ± 0.0000 | 640.7005 ± 0.0000 | 1787.2815 ± 0.0000 | 0.7222 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

