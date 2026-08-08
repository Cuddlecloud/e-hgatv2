# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7856 ± 0.0000 | 1511.3744 ± 0.0000 | 241.3989 ± 0.0000 | 1.0720 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.6765 ± 0.0000 | 443.7848 ± 0.0000 | 334.9126 ± 0.0000 | 0.9618 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.2635 ± 0.0000 | 1535.4784 ± 0.0000 | 1385.5027 ± 0.0000 | 1.0048 ± 0.0000 | 16400 |
| mp-BRKGA | 0.7348 ± 0.0000 | 1235.6911 ± 0.0000 | 251.2815 ± 0.0000 | 1.0335 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.3747 ± 0.0000 | 698.1636 ± 0.0000 | 828.0788 ± 0.0000 | 0.8218 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

