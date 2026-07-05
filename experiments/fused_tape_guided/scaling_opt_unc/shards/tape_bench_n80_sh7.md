# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.4467 ± 0.0000 | 1152.4662 ± 0.0000 | 2023.9891 ± 0.0000 | 0.9705 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.5214 ± 0.0000 | 1139.1182 ± 0.0000 | 1280.8796 ± 0.0000 | 0.8588 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.2629 ± 0.0000 | 2361.3666 ± 0.0000 | 2732.2782 ± 0.0000 | 0.9350 ± 0.0000 | 65600 |
| mp-BRKGA | 0.2157 ± 0.0000 | 4996.4266 ± 0.0000 | 2314.4359 ± 0.0000 | 0.8682 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.0404 ± 0.0000 | 2484.0427 ± 0.0000 | 5192.5895 ± 0.0000 | 1.0127 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

