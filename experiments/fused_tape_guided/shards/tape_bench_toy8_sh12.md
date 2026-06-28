# Faithful-guidance study -- toy:8 (N=8, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 40x4 = GAT/BRKGA 160/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9490 ± 0.0300 | 10.0146 ± 10.0036 | 33.4963 ± 17.7158 | 1.0032 ± 0.1079 | 6560 |
| E-HGATv2-attn | 0.9589 ± 0.0497 | 19.5379 ± 27.9495 | 25.7580 ± 43.2030 | 0.9436 ± 0.1050 | 6560 |
| NSGA-II (random) | 0.9183 ± 0.0342 | 38.5432 ± 33.0791 | 48.5921 ± 26.2904 | 0.9695 ± 0.1014 | 6560 |
| mp-BRKGA | 0.9217 ± 0.0315 | 48.1716 ± 46.0824 | 39.6254 ± 23.1000 | 0.8919 ± 0.1321 | 6560 |
| single-pop BRKGA | 0.9136 ± 0.0332 | 28.0867 ± 33.7552 | 45.6209 ± 24.9068 | 1.0540 ± 0.1608 | 6560 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.800 | -0.023 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.990** |
| random baseline | 0.125 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 8.978. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

