# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8096 ± 0.0000 | 26.7491 ± 0.0000 | 80.4633 ± 0.0000 | 0.8778 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9436 ± 0.0000 | 10.1227 ± 0.0000 | 13.3978 ± 0.0000 | 1.1886 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.7324 ± 0.0000 | 99.7226 ± 0.0000 | 114.7844 ± 0.0000 | 1.0929 ± 0.0000 | 8200 |
| mp-BRKGA | 0.7393 ± 0.0000 | 181.4030 ± 0.0000 | 85.9361 ± 0.0000 | 1.0006 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.9123 ± 0.0000 | 25.4657 ± 0.0000 | 21.3228 ± 0.0000 | 1.0618 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

