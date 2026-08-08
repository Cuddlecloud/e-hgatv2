# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8383 ± 0.0000 | 137.8551 ± 0.0000 | 69.6556 ± 0.0000 | 1.0185 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9577 ± 0.0000 | 0.7141 ± 0.0000 | 14.8108 ± 0.0000 | 0.9091 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.7154 ± 0.0000 | 299.0024 ± 0.0000 | 127.1271 ± 0.0000 | 0.8847 ± 0.0000 | 8200 |
| mp-BRKGA | 0.6778 ± 0.0000 | 251.2845 ± 0.0000 | 142.9856 ± 0.0000 | 1.0719 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8283 ± 0.0000 | 74.9327 ± 0.0000 | 70.5047 ± 0.0000 | 0.9396 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

