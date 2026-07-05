# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9056 ± 0.0000 | 32.6011 ± 0.0000 | 89.4837 ± 0.0000 | 1.2799 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.8170 ± 0.0000 | 137.9465 ± 0.0000 | 140.6366 ± 0.0000 | 0.9720 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.5822 ± 0.0000 | 361.9353 ± 0.0000 | 390.9069 ± 0.0000 | 0.7986 ± 0.0000 | 16400 |
| mp-BRKGA | 0.6956 ± 0.0000 | 179.5227 ± 0.0000 | 211.0376 ± 0.0000 | 0.8756 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.6252 ± 0.0000 | 331.3887 ± 0.0000 | 204.5042 ± 0.0000 | 0.7483 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

