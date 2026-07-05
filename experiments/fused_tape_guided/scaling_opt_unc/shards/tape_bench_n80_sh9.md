# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.4078 ± 0.0000 | 2523.2266 ± 0.0000 | 2485.7647 ± 0.0000 | 0.9336 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.6669 ± 0.0000 | 994.9585 ± 0.0000 | 745.4069 ± 0.0000 | 1.0014 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.2017 ± 0.0000 | 1517.3180 ± 0.0000 | 3306.1902 ± 0.0000 | 0.8945 ± 0.0000 | 65600 |
| mp-BRKGA | 0.2719 ± 0.0000 | 3620.9764 ± 0.0000 | 2092.2408 ± 0.0000 | 0.7914 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.0519 ± 0.0000 | 3539.0193 ± 0.0000 | 4738.5396 ± 0.0000 | 0.8412 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

