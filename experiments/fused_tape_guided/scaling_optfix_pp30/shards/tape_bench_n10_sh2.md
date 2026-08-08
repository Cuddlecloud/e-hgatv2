# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9765 ± 0.0000 | 9.1319 ± 0.0000 | 9.0554 ± 0.0000 | 0.8802 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.8567 ± 0.0000 | 100.1236 ± 0.0000 | 42.4811 ± 0.0000 | 1.1655 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.6849 ± 0.0000 | 236.8495 ± 0.0000 | 115.3892 ± 0.0000 | 0.8127 ± 0.0000 | 16400 |
| mp-BRKGA | 0.8627 ± 0.0000 | 57.1950 ± 0.0000 | 48.5278 ± 0.0000 | 1.0358 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.9226 ± 0.0000 | 8.2028 ± 0.0000 | 32.0739 ± 0.0000 | 0.9030 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

