# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8797 ± 0.0000 | 384.8521 ± 0.0000 | 243.4947 ± 0.0000 | 0.9882 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.8237 ± 0.0000 | 293.1680 ± 0.0000 | 346.7253 ± 0.0000 | 0.9327 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.4900 ± 0.0000 | 1305.8390 ± 0.0000 | 1489.4319 ± 0.0000 | 0.8364 ± 0.0000 | 32800 |
| mp-BRKGA | 0.7459 ± 0.0000 | 1255.2072 ± 0.0000 | 454.4983 ± 0.0000 | 0.8644 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.4186 ± 0.0000 | 807.1709 ± 0.0000 | 1801.9966 ± 0.0000 | 0.9142 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

