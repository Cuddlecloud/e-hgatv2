# Faithful-guidance study -- toy:5 (N=5, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 25x4 = GAT/BRKGA 100/gen). Reference: exact Oracle. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9815 ± 0.0381 | 1.4289 ± 1.8058 | 11.8936 ± 31.8070 | 0.9331 ± 0.0495 | 4100 |
| E-HGATv2-attn | 0.9736 ± 0.0265 | 1.9178 ± 1.3078 | 13.5725 ± 28.3189 | 0.9729 ± 0.0312 | 4100 |
| NSGA-II (random) | 0.9665 ± 0.0325 | 2.1960 ± 2.5401 | 22.7238 ± 34.2404 | 0.9269 ± 0.0712 | 4100 |
| mp-BRKGA | 0.9209 ± 0.0506 | 29.3795 ± 34.2707 | 34.8803 ± 26.2241 | 0.8617 ± 0.1988 | 4100 |
| single-pop BRKGA | 0.9571 ± 0.0324 | 6.0725 ± 8.0917 | 26.0606 ± 34.5448 | 0.9523 ± 0.2333 | 4100 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.062 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.980** |
| random baseline | 0.200 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 8.114. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

