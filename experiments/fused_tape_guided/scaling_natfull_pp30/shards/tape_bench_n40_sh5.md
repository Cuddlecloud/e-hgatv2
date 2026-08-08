# Faithful-guidance study -- toy:40 (N=40, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7071 ± 0.0000 | 331.0092 ± 0.0000 | 685.0832 ± 0.0000 | 0.9805 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.7054 ± 0.0000 | 53.4498 ± 0.0000 | 691.8837 ± 0.0000 | 0.7519 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.6012 ± 0.0000 | 685.4295 ± 0.0000 | 844.4654 ± 0.0000 | 0.8646 ± 0.0000 | 32800 |
| mp-BRKGA | 0.9526 ± 0.0000 | 375.2273 ± 0.0000 | 36.6793 ± 0.0000 | 0.8676 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.3295 ± 0.0000 | 1492.0955 ± 0.0000 | 1738.4649 ± 0.0000 | 0.9257 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.633 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.902** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 75.981. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

