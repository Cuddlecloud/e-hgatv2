# Faithful-guidance study -- toy:8 (N=8, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 40x4 = GAT/BRKGA 160/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9358 ± 0.0406 | 17.5479 ± 15.4952 | 43.0799 ± 57.2072 | 1.0416 ± 0.1648 | 6560 |
| E-HGATv2-attn | 0.9508 ± 0.0186 | 13.5014 ± 9.7513 | 26.8776 ± 32.0694 | 1.0052 ± 0.1643 | 6560 |
| NSGA-II (random) | 0.9055 ± 0.0359 | 40.1048 ± 11.3063 | 50.8470 ± 34.7309 | 0.8685 ± 0.0578 | 6560 |
| mp-BRKGA | 0.8594 ± 0.0458 | 65.9038 ± 62.4105 | 95.7464 ± 56.0569 | 0.8416 ± 0.1867 | 6560 |
| single-pop BRKGA | 0.9124 ± 0.0334 | 30.5012 ± 29.7202 | 55.2222 ± 34.5535 | 0.9131 ± 0.2600 | 6560 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.800 | -0.023 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.990** |
| random baseline | 0.125 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 8.978. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

