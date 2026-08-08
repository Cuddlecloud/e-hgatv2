# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9761 ± 0.0000 | 10.2294 ± 0.0000 | 10.9330 ± 0.0000 | 0.8112 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.9911 ± 0.0000 | 2.5220 ± 0.0000 | 3.4845 ± 0.0000 | 0.9017 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.9102 ± 0.0000 | 31.9360 ± 0.0000 | 40.1637 ± 0.0000 | 1.1663 ± 0.0000 | 16400 |
| mp-BRKGA | 0.8735 ± 0.0000 | 172.7667 ± 0.0000 | 57.7812 ± 0.0000 | 1.0245 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.8845 ± 0.0000 | 45.0138 ± 0.0000 | 71.7450 ± 0.0000 | 0.8633 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

