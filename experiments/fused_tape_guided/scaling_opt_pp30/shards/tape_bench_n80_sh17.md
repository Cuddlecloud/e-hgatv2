# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7963 ± 0.0000 | 146.2357 ± 0.0000 | 762.0311 ± 0.0000 | 0.6981 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.6815 ± 0.0000 | 405.6566 ± 0.0000 | 895.3938 ± 0.0000 | 1.0138 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.1471 ± 0.0000 | 3087.0884 ± 0.0000 | 3741.2935 ± 0.0000 | 0.9948 ± 0.0000 | 65600 |
| mp-BRKGA | 0.4082 ± 0.0000 | 1321.2190 ± 0.0000 | 1645.3445 ± 0.0000 | 0.7772 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.0775 ± 0.0000 | 2659.6111 ± 0.0000 | 3934.6872 ± 0.0000 | 0.8861 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

