# Faithful-guidance study -- toy:10 (N=10, coupled)

_5 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8594 ± 0.0884 | 71.3040 ± 54.4657 | 98.6038 ± 72.1176 | 0.9564 ± 0.0509 | 8200 |
| E-HGATv2-attn | 0.9189 ± 0.0749 | 49.9438 ± 67.8191 | 44.8263 ± 42.3037 | 1.0534 ± 0.0792 | 8200 |
| NSGA-II (random) | 0.7411 ± 0.1279 | 152.6367 ± 104.6540 | 194.9906 ± 140.0969 | 0.9867 ± 0.0754 | 8200 |
| mp-BRKGA | 0.7978 ± 0.0836 | 179.4031 ± 115.7773 | 115.1948 ± 68.2108 | 1.0033 ± 0.1118 | 8200 |
| single-pop BRKGA | 0.7906 ± 0.1068 | 94.4250 ± 87.7365 | 148.2489 ± 108.2097 | 0.9280 ± 0.1153 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.087 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 34.291. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

