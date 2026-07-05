# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8785 ± 0.0000 | 118.3024 ± 0.0000 | 776.1436 ± 0.0000 | 0.9662 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.8582 ± 0.0000 | 255.7155 ± 0.0000 | 282.2576 ± 0.0000 | 0.9188 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.3935 ± 0.0000 | 1094.0529 ± 0.0000 | 3736.4996 ± 0.0000 | 0.9029 ± 0.0000 | 65600 |
| mp-BRKGA | 0.4716 ± 0.0000 | 1053.0360 ± 0.0000 | 2171.5178 ± 0.0000 | 0.6472 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.3528 ± 0.0000 | 1213.1047 ± 0.0000 | 4187.7693 ± 0.0000 | 0.7920 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

