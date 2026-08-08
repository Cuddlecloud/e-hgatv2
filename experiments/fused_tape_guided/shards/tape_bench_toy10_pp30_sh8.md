# Faithful-guidance study -- toy:10 (N=10, coupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8785 ± 0.0819 | 59.7365 ± 53.5558 | 50.6438 ± 35.4664 | 1.0596 ± 0.0665 | 8200 |
| E-HGATv2-attn | 0.9134 ± 0.0540 | 72.4844 ± 116.2336 | 35.8646 ± 24.6374 | 1.0180 ± 0.1692 | 8200 |
| NSGA-II (random) | 0.8205 ± 0.1567 | 65.2259 ± 81.0187 | 75.9127 ± 65.8594 | 0.9155 ± 0.2013 | 8200 |
| mp-BRKGA | 0.7814 ± 0.1159 | 138.8299 ± 87.4263 | 91.3591 ± 57.3238 | 1.0431 ± 0.0869 | 8200 |
| single-pop BRKGA | 0.7774 ± 0.1672 | 126.3928 ± 179.6525 | 98.2580 ± 78.4223 | 0.9339 ± 0.1900 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

