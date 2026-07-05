# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7998 ± 0.0000 | 251.6382 ± 0.0000 | 1199.8724 ± 0.0000 | 0.9162 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.7690 ± 0.0000 | 278.8760 ± 0.0000 | 737.5181 ± 0.0000 | 0.9255 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.4432 ± 0.0000 | 1152.1035 ± 0.0000 | 2900.7316 ± 0.0000 | 0.9242 ± 0.0000 | 65600 |
| mp-BRKGA | 0.6550 ± 0.0000 | 696.3182 ± 0.0000 | 774.6778 ± 0.0000 | 0.7224 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.3709 ± 0.0000 | 1065.8845 ± 0.0000 | 3759.3284 ± 0.0000 | 0.8265 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

