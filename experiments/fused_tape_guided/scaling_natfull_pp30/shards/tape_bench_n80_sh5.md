# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7830 ± 0.0000 | 53.6857 ± 0.0000 | 907.8136 ± 0.0000 | 0.8368 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.8077 ± 0.0000 | 193.4930 ± 0.0000 | 484.5580 ± 0.0000 | 1.0772 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.4580 ± 0.0000 | 736.8295 ± 0.0000 | 2325.8123 ± 0.0000 | 0.8513 ± 0.0000 | 65600 |
| mp-BRKGA | 0.7593 ± 0.0000 | 1098.3280 ± 0.0000 | 432.7946 ± 0.0000 | 0.6833 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.3138 ± 0.0000 | 2021.4196 ± 0.0000 | 3068.4760 ± 0.0000 | 0.7471 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

