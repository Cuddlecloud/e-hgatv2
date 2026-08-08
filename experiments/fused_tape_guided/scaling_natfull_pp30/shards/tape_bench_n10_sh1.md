# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9617 ± 0.0000 | 8.7066 ± 0.0000 | 7.2666 ± 0.0000 | 1.0798 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9300 ± 0.0000 | 23.9830 ± 0.0000 | 14.2930 ± 0.0000 | 1.0995 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.9545 ± 0.0000 | 24.3893 ± 0.0000 | 80.8506 ± 0.0000 | 1.0102 ± 0.0000 | 8200 |
| mp-BRKGA | 0.8330 ± 0.0000 | 78.1039 ± 0.0000 | 75.3427 ± 0.0000 | 0.8658 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8457 ± 0.0000 | 59.1964 ± 0.0000 | 199.5726 ± 0.0000 | 0.9870 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

