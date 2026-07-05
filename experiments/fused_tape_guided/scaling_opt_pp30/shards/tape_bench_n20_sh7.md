# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7761 ± 0.0000 | 90.6816 ± 0.0000 | 245.5104 ± 0.0000 | 0.8862 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.9544 ± 0.0000 | 32.4151 ± 0.0000 | 62.7819 ± 0.0000 | 0.9367 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.4726 ± 0.0000 | 338.0482 ± 0.0000 | 752.4376 ± 0.0000 | 0.9546 ± 0.0000 | 16400 |
| mp-BRKGA | 0.7691 ± 0.0000 | 712.9068 ± 0.0000 | 261.7856 ± 0.0000 | 0.9852 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.5774 ± 0.0000 | 238.3343 ± 0.0000 | 554.0286 ± 0.0000 | 0.8439 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

