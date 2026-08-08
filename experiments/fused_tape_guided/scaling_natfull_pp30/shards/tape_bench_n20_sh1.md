# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9558 ± 0.0000 | 0.0000 ± 0.0000 | 78.4970 ± 0.0000 | 1.3318 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7514 ± 0.0000 | 130.5663 ± 0.0000 | 182.4179 ± 0.0000 | 0.8796 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.6064 ± 0.0000 | 374.9035 ± 0.0000 | 403.5692 ± 0.0000 | 0.8494 ± 0.0000 | 16400 |
| mp-BRKGA | 0.5268 ± 0.0000 | 580.2224 ± 0.0000 | 558.7178 ± 0.0000 | 1.0784 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.6564 ± 0.0000 | 240.5469 ± 0.0000 | 297.2979 ± 0.0000 | 0.7788 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

