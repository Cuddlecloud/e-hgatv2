# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7995 ± 0.0000 | 309.8759 ± 0.0000 | 1238.0806 ± 0.0000 | 1.0135 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.7835 ± 0.0000 | 372.4979 ± 0.0000 | 1058.9441 ± 0.0000 | 1.0762 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.3850 ± 0.0000 | 1089.4835 ± 0.0000 | 3754.8131 ± 0.0000 | 0.8465 ± 0.0000 | 65600 |
| mp-BRKGA | 0.5362 ± 0.0000 | 962.8762 ± 0.0000 | 1364.6528 ± 0.0000 | 0.7887 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.3606 ± 0.0000 | 1043.2185 ± 0.0000 | 3779.4861 ± 0.0000 | 0.8994 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

