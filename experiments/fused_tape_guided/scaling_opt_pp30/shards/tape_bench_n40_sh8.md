# Faithful-guidance study -- toy:40 (N=40, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.6997 ± 0.0000 | 404.3831 ± 0.0000 | 617.5979 ± 0.0000 | 0.9644 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.9659 ± 0.0000 | 35.0824 ± 0.0000 | 37.3087 ± 0.0000 | 0.8092 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.4932 ± 0.0000 | 468.6082 ± 0.0000 | 1831.9121 ± 0.0000 | 0.9114 ± 0.0000 | 32800 |
| mp-BRKGA | 0.8970 ± 0.0000 | 27.8250 ± 0.0000 | 65.7461 ± 0.0000 | 1.0236 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.3977 ± 0.0000 | 836.6301 ± 0.0000 | 1804.7702 ± 0.0000 | 0.7181 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.633 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.902** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 75.981. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

