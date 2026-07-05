# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9434 ± 0.0000 | 0.3720 ± 0.0000 | 491.9955 ± 0.0000 | 1.0438 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.7342 ± 0.0000 | 845.8913 ± 0.0000 | 1443.8515 ± 0.0000 | 0.9036 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.5010 ± 0.0000 | 879.5677 ± 0.0000 | 4031.8700 ± 0.0000 | 0.9121 ± 0.0000 | 65600 |
| mp-BRKGA | 0.5532 ± 0.0000 | 913.6186 ± 0.0000 | 1226.4018 ± 0.0000 | 0.6714 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.3579 ± 0.0000 | 1076.8553 ± 0.0000 | 4892.6343 ± 0.0000 | 0.7552 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

