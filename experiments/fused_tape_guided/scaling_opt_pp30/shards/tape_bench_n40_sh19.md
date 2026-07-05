# Faithful-guidance study -- toy:40 (N=40, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9568 ± 0.0000 | 0.0000 ± 0.0000 | 67.0259 ± 0.0000 | 0.8712 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.7093 ± 0.0000 | 801.1447 ± 0.0000 | 381.0270 ± 0.0000 | 1.0141 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.1981 ± 0.0000 | 1607.0400 ± 0.0000 | 1817.4401 ± 0.0000 | 0.8559 ± 0.0000 | 32800 |
| mp-BRKGA | 0.5820 ± 0.0000 | 1844.8050 ± 0.0000 | 632.1879 ± 0.0000 | 0.9490 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.2060 ± 0.0000 | 1172.0806 ± 0.0000 | 1784.9628 ± 0.0000 | 0.7957 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.633 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.902** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 75.981. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

