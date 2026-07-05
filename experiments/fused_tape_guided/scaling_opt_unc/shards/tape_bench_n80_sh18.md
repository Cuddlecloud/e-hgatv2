# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.4971 ± 0.0000 | 689.2399 ± 0.0000 | 1927.3671 ± 0.0000 | 0.8603 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.5285 ± 0.0000 | 899.0558 ± 0.0000 | 1520.6044 ± 0.0000 | 0.8736 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.1091 ± 0.0000 | 2822.9354 ± 0.0000 | 3346.4129 ± 0.0000 | 0.8594 ± 0.0000 | 65600 |
| mp-BRKGA | 0.4957 ± 0.0000 | 2473.5403 ± 0.0000 | 1042.1028 ± 0.0000 | 0.8068 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.0346 ± 0.0000 | 3244.9144 ± 0.0000 | 5254.6090 ± 0.0000 | 0.8934 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

