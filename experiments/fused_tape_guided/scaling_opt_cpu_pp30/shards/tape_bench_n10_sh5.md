# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8273 ± 0.0000 | 143.2522 ± 0.0000 | 75.2182 ± 0.0000 | 1.0185 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9451 ± 0.0000 | 5.5680 ± 0.0000 | 18.9819 ± 0.0000 | 0.9091 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.7060 ± 0.0000 | 303.1558 ± 0.0000 | 131.2674 ± 0.0000 | 0.8847 ± 0.0000 | 8200 |
| mp-BRKGA | 0.6689 ± 0.0000 | 255.2124 ± 0.0000 | 149.1449 ± 0.0000 | 1.0719 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8174 ± 0.0000 | 78.3645 ± 0.0000 | 76.8314 ± 0.0000 | 0.9396 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

