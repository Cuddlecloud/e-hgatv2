# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7949 ± 0.0000 | 437.1604 ± 0.0000 | 1039.2642 ± 0.0000 | 0.9252 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.7865 ± 0.0000 | 279.9822 ± 0.0000 | 1053.4151 ± 0.0000 | 0.8963 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.3716 ± 0.0000 | 1162.7361 ± 0.0000 | 3842.1293 ± 0.0000 | 0.7754 ± 0.0000 | 65600 |
| mp-BRKGA | 0.4395 ± 0.0000 | 913.5618 ± 0.0000 | 2181.6109 ± 0.0000 | 0.8837 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.3734 ± 0.0000 | 1037.7743 ± 0.0000 | 3673.6154 ± 0.0000 | 0.8134 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

