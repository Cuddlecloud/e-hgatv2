# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7781 ± 0.0000 | 223.4360 ± 0.0000 | 410.1616 ± 0.0000 | 0.9238 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.9836 ± 0.0000 | 16.9994 ± 0.0000 | 37.2411 ± 0.0000 | 0.8892 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.5399 ± 0.0000 | 437.1773 ± 0.0000 | 1395.9411 ± 0.0000 | 0.8862 ± 0.0000 | 32800 |
| mp-BRKGA | 0.7143 ± 0.0000 | 248.9662 ± 0.0000 | 343.4828 ± 0.0000 | 0.8727 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.4441 ± 0.0000 | 680.7407 ± 0.0000 | 1753.3044 ± 0.0000 | 0.8131 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

