# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8864 ± 0.0000 | 94.5677 ± 0.0000 | 328.3609 ± 0.0000 | 0.9227 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.8471 ± 0.0000 | 123.6720 ± 0.0000 | 385.4521 ± 0.0000 | 0.8892 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.5642 ± 0.0000 | 496.0907 ± 0.0000 | 1621.6541 ± 0.0000 | 0.8035 ± 0.0000 | 32800 |
| mp-BRKGA | 0.8777 ± 0.0000 | 148.7526 ± 0.0000 | 384.0138 ± 0.0000 | 0.7064 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.5102 ± 0.0000 | 727.0779 ± 0.0000 | 1878.4098 ± 0.0000 | 0.8882 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

