# Faithful-guidance study -- toy:10 (N=10, coupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9805 ± 0.2217 | 27.1184 ± 49.8545 | 25.6062 ± 23.4887 | 0.9225 ± 0.0906 | 8200 |
| E-HGATv2-attn | 1.0441 ± 0.1685 | 29.3805 ± 42.3202 | 10.6573 ± 10.3504 | 0.9717 ± 0.0914 | 8200 |
| NSGA-II (random) | 0.8397 ± 0.1408 | 192.3534 ± 186.0256 | 45.5309 ± 44.3890 | 0.9990 ± 0.1268 | 8200 |
| mp-BRKGA | 0.7557 ± 0.1285 | 190.4966 ± 197.3791 | 72.0539 ± 51.4200 | 1.0412 ± 0.0828 | 8200 |
| single-pop BRKGA | 0.9177 ± 0.1507 | 85.1099 ± 98.9473 | 30.1801 ± 26.4923 | 1.0686 ± 0.1858 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

