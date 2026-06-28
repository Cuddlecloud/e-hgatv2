# Faithful-guidance study -- toy:10 (N=10, coupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 1.0690 ± 0.1592 | 27.6398 ± 57.2603 | 12.6506 ± 12.2800 | 1.0158 ± 0.1097 | 8200 |
| E-HGATv2-attn | 1.0907 ± 0.0593 | 20.9315 ± 30.3525 | 8.3591 ± 5.8089 | 1.0795 ± 0.2256 | 8200 |
| NSGA-II (random) | 0.8905 ± 0.1775 | 38.2064 ± 46.8558 | 50.1517 ± 38.0507 | 0.9837 ± 0.1755 | 8200 |
| mp-BRKGA | 0.8896 ± 0.2044 | 100.2990 ± 60.6346 | 38.8955 ± 39.2342 | 1.0576 ± 0.0754 | 8200 |
| single-pop BRKGA | 0.8569 ± 0.2090 | 44.8056 ± 61.0989 | 49.3953 ± 40.6555 | 1.0406 ± 0.2252 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

