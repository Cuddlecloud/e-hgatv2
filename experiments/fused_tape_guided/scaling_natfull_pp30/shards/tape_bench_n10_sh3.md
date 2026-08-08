# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8793 ± 0.0000 | 53.7172 ± 0.0000 | 41.0345 ± 0.0000 | 0.9804 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.8462 ± 0.0000 | 44.6147 ± 0.0000 | 69.3122 ± 0.0000 | 0.8450 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.7122 ± 0.0000 | 184.8735 ± 0.0000 | 142.5367 ± 0.0000 | 1.0688 ± 0.0000 | 8200 |
| mp-BRKGA | 0.9320 ± 0.0000 | 283.4988 ± 0.0000 | 36.1353 ± 0.0000 | 1.0997 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8312 ± 0.0000 | 167.7515 ± 0.0000 | 61.0898 ± 0.0000 | 0.8338 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

