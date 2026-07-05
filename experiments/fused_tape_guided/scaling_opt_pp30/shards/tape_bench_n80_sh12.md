# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8289 ± 0.0000 | 213.1215 ± 0.0000 | 1206.2977 ± 0.0000 | 0.9463 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.8155 ± 0.0000 | 217.3316 ± 0.0000 | 938.7090 ± 0.0000 | 0.9121 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.5807 ± 0.0000 | 658.3808 ± 0.0000 | 2525.9913 ± 0.0000 | 0.9739 ± 0.0000 | 65600 |
| mp-BRKGA | 0.5893 ± 0.0000 | 732.5314 ± 0.0000 | 1159.8893 ± 0.0000 | 1.0383 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.4202 ± 0.0000 | 1028.5367 ± 0.0000 | 3461.9770 ± 0.0000 | 0.7581 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

