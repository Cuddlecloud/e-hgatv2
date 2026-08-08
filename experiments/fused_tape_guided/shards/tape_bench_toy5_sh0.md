# Faithful-guidance study -- toy:5 (N=5, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 25x4 = GAT/BRKGA 100/gen). Reference: exact Oracle. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9740 ± 0.0373 | 1.1691 ± 1.4497 | 21.3291 ± 36.0291 | 0.9174 ± 0.0673 | 4100 |
| E-HGATv2-attn | 0.9708 ± 0.0347 | 4.5847 ± 12.0357 | 13.5859 ± 30.0284 | 1.0104 ± 0.1710 | 4100 |
| NSGA-II (random) | 0.9783 ± 0.0088 | 1.5893 ± 1.6589 | 6.2094 ± 3.5055 | 0.9617 ± 0.0530 | 4100 |
| mp-BRKGA | 0.9259 ± 0.0343 | 15.5467 ± 7.4917 | 46.3105 ± 30.1136 | 0.7629 ± 0.0689 | 4100 |
| single-pop BRKGA | 0.9810 ± 0.0118 | 3.4826 ± 2.6196 | 6.1678 ± 3.1281 | 0.8510 ± 0.1403 | 4100 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.062 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.980** |
| random baseline | 0.200 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 8.114. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

