# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7471 ± 0.0000 | 530.8289 ± 0.0000 | 425.7923 ± 0.0000 | 0.9743 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.5209 ± 0.0000 | 1319.2965 ± 0.0000 | 1428.6271 ± 0.0000 | 0.8958 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0000 ± 0.0000 | 4619.0686 ± 0.0000 | 6135.3130 ± 0.0000 | 0.8834 ± 0.0000 | 131200 |
| mp-BRKGA | 0.0228 ± 0.0000 | 4840.1876 ± 0.0000 | 2512.1787 ± 0.0000 | 0.7973 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0000 ± 0.0000 | 6599.9927 ± 0.0000 | 6628.2383 ± 0.0000 | 0.9276 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

