# Faithful-guidance study -- toy:40 (N=40, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9581 ± 0.0000 | 49.8648 ± 0.0000 | 80.9742 ± 0.0000 | 0.9624 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.9123 ± 0.0000 | 7.5476 ± 0.0000 | 265.0400 ± 0.0000 | 1.1057 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.4381 ± 0.0000 | 656.0376 ± 0.0000 | 2196.4874 ± 0.0000 | 0.8562 ± 0.0000 | 32800 |
| mp-BRKGA | 0.7612 ± 0.0000 | 369.1184 ± 0.0000 | 382.5328 ± 0.0000 | 1.0119 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.5784 ± 0.0000 | 425.7414 ± 0.0000 | 1375.6052 ± 0.0000 | 0.7066 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.633 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.902** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 75.981. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

