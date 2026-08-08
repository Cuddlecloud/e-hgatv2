# Faithful-guidance study -- toy:40 (N=40, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8941 ± 0.0000 | 0.0000 ± 0.0000 | 771.5717 ± 0.0000 | 0.9773 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.7477 ± 0.0000 | 279.9962 ± 0.0000 | 1317.8803 ± 0.0000 | 0.9055 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.6054 ± 0.0000 | 376.4182 ± 0.0000 | 1846.3959 ± 0.0000 | 0.9152 ± 0.0000 | 32800 |
| mp-BRKGA | 0.9156 ± 0.0000 | 59.6151 ± 0.0000 | 92.5555 ± 0.0000 | 0.9699 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.5981 ± 0.0000 | 431.0505 ± 0.0000 | 1878.6574 ± 0.0000 | 0.9787 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.633 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.902** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 75.981. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

