# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7653 ± 0.0000 | 460.1242 ± 0.0000 | 1476.6867 ± 0.0000 | 1.0055 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.8639 ± 0.0000 | 142.4040 ± 0.0000 | 378.9742 ± 0.0000 | 0.9383 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.3170 ± 0.0000 | 1167.3370 ± 0.0000 | 3842.1951 ± 0.0000 | 0.9152 ± 0.0000 | 65600 |
| mp-BRKGA | 0.4679 ± 0.0000 | 1404.4077 ± 0.0000 | 1308.7432 ± 0.0000 | 0.8591 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.2990 ± 0.0000 | 1168.9017 ± 0.0000 | 3826.5540 ± 0.0000 | 0.7977 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

