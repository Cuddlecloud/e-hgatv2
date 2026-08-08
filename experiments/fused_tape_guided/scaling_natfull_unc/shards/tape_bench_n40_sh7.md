# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8609 ± 0.0000 | 174.4216 ± 0.0000 | 415.2185 ± 0.0000 | 0.8852 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.9382 ± 0.0000 | 51.3553 ± 0.0000 | 224.2973 ± 0.0000 | 0.8146 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.6549 ± 0.0000 | 303.5538 ± 0.0000 | 731.9411 ± 0.0000 | 0.8471 ± 0.0000 | 32800 |
| mp-BRKGA | 0.8461 ± 0.0000 | 76.7411 ± 0.0000 | 104.0720 ± 0.0000 | 0.7884 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.5658 ± 0.0000 | 638.2140 ± 0.0000 | 981.2633 ± 0.0000 | 0.7664 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

