# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8489 ± 0.0000 | 327.0467 ± 0.0000 | 599.8322 ± 0.0000 | 0.8261 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.9289 ± 0.0000 | 13.9792 ± 0.0000 | 90.1084 ± 0.0000 | 0.8998 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0807 ± 0.0000 | 2112.1312 ± 0.0000 | 5349.8955 ± 0.0000 | 0.8167 ± 0.0000 | 131200 |
| mp-BRKGA | 0.1119 ± 0.0000 | 2662.2070 ± 0.0000 | 5008.9937 ± 0.0000 | 0.8383 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0716 ± 0.0000 | 2278.5422 ± 0.0000 | 5354.0987 ± 0.0000 | 0.7720 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

