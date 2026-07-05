# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7520 ± 0.0000 | 198.8186 ± 0.0000 | 226.8205 ± 0.0000 | 1.0064 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.8670 ± 0.0000 | 254.3265 ± 0.0000 | 94.9579 ± 0.0000 | 1.0781 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.5365 ± 0.0000 | 466.5493 ± 0.0000 | 454.0160 ± 0.0000 | 0.7248 ± 0.0000 | 16400 |
| mp-BRKGA | 0.7570 ± 0.0000 | 583.3996 ± 0.0000 | 151.7804 ± 0.0000 | 1.0458 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.8421 ± 0.0000 | 104.2055 ± 0.0000 | 93.7052 ± 0.0000 | 1.0684 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

