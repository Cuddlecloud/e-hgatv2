# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9439 ± 0.0000 | 163.3582 ± 0.0000 | 167.4278 ± 0.0000 | 0.8258 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.7627 ± 0.0000 | 1118.3192 ± 0.0000 | 1072.5703 ± 0.0000 | 0.9444 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.3043 ± 0.0000 | 2382.7338 ± 0.0000 | 4977.9462 ± 0.0000 | 0.9232 ± 0.0000 | 131200 |
| mp-BRKGA | 0.3984 ± 0.0000 | 3230.7807 ± 0.0000 | 3360.3700 ± 0.0000 | 0.7573 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.2952 ± 0.0000 | 2209.3856 ± 0.0000 | 5262.8248 ± 0.0000 | 0.7383 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

