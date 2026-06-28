# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9805 ± 0.1002 | 7.6325 ± 18.3688 | 51.0282 ± 71.4289 | 1.0176 ± 0.1410 | 8200 |
| E-HGATv2-attn | 1.0289 ± 0.0464 | 4.1976 ± 4.0609 | 4.9569 ± 3.3000 | 0.9596 ± 0.1216 | 8200 |
| NSGA-II (random) | 0.9832 ± 0.0438 | 5.6595 ± 6.8469 | 39.8163 ± 53.3420 | 0.8840 ± 0.0226 | 8200 |
| mp-BRKGA | 0.9200 ± 0.0407 | 33.9098 ± 23.8079 | 46.8667 ± 56.1153 | 0.8848 ± 0.2395 | 8200 |
| single-pop BRKGA | 0.9581 ± 0.1039 | 12.5025 ± 35.0027 | 68.7538 ± 53.6183 | 1.0127 ± 0.1874 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

