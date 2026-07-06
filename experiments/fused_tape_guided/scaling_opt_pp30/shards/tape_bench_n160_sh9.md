# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8950 ± 0.0000 | 247.5013 ± 0.0000 | 393.7787 ± 0.0000 | 0.8319 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.8146 ± 0.0000 | 337.5383 ± 0.0000 | 415.2100 ± 0.0000 | 0.8131 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.2399 ± 0.0000 | 1806.9330 ± 0.0000 | 4112.7289 ± 0.0000 | 0.8947 ± 0.0000 | 131200 |
| mp-BRKGA | 0.2292 ± 0.0000 | 2421.5041 ± 0.0000 | 3138.5698 ± 0.0000 | 0.8950 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.1687 ± 0.0000 | 2577.2253 ± 0.0000 | 3927.4623 ± 0.0000 | 0.8014 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

