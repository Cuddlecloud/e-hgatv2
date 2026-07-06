# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9178 ± 0.0000 | 69.0979 ± 0.0000 | 277.1964 ± 0.0000 | 0.8083 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.9047 ± 0.0000 | 407.0180 ± 0.0000 | 377.4268 ± 0.0000 | 0.7797 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.3181 ± 0.0000 | 2304.9451 ± 0.0000 | 4683.9891 ± 0.0000 | 0.8081 ± 0.0000 | 131200 |
| mp-BRKGA | 0.3736 ± 0.0000 | 2474.1942 ± 0.0000 | 3151.1517 ± 0.0000 | 0.7817 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.2987 ± 0.0000 | 2453.0816 ± 0.0000 | 4902.1178 ± 0.0000 | 0.7897 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

