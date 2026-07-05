# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9007 ± 0.0000 | 99.5214 ± 0.0000 | 299.2442 ± 0.0000 | 1.0241 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.9485 ± 0.0000 | 36.5761 ± 0.0000 | 173.7774 ± 0.0000 | 0.9598 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.5671 ± 0.0000 | 604.5049 ± 0.0000 | 1702.2946 ± 0.0000 | 0.8542 ± 0.0000 | 32800 |
| mp-BRKGA | 0.8606 ± 0.0000 | 113.7470 ± 0.0000 | 284.6340 ± 0.0000 | 0.9249 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.5304 ± 0.0000 | 640.5605 ± 0.0000 | 1843.1249 ± 0.0000 | 0.8079 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

