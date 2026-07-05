# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8829 ± 0.0000 | 78.1015 ± 0.0000 | 53.1772 ± 0.0000 | 1.1439 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.8429 ± 0.0000 | 42.6819 ± 0.0000 | 65.1778 ± 0.0000 | 1.0772 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.8358 ± 0.0000 | 119.8431 ± 0.0000 | 68.5282 ± 0.0000 | 1.0578 ± 0.0000 | 8200 |
| mp-BRKGA | 0.5886 ± 0.0000 | 334.0060 ± 0.0000 | 202.7041 ± 0.0000 | 0.9741 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.7519 ± 0.0000 | 135.6651 ± 0.0000 | 100.4726 ± 0.0000 | 0.8952 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

