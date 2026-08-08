# Faithful-guidance study -- toy:8 (N=8, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 40x4 = GAT/BRKGA 160/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9207 ± 0.0676 | 22.9888 ± 32.0091 | 48.3991 ± 58.9455 | 0.9865 ± 0.1419 | 6560 |
| E-HGATv2-attn | 0.9518 ± 0.0221 | 15.4477 ± 14.8421 | 19.7766 ± 12.2294 | 0.9925 ± 0.0623 | 6560 |
| NSGA-II (random) | 0.9108 ± 0.0547 | 31.8441 ± 32.8362 | 43.1571 ± 33.9152 | 0.9501 ± 0.1506 | 6560 |
| mp-BRKGA | 0.8932 ± 0.0313 | 70.0979 ± 61.4243 | 48.9043 ± 22.9994 | 0.9287 ± 0.0360 | 6560 |
| single-pop BRKGA | 0.9147 ± 0.0457 | 23.1498 ± 21.1123 | 43.5151 ± 31.6561 | 0.9751 ± 0.2063 | 6560 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.800 | -0.023 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.990** |
| random baseline | 0.125 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 8.978. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

