# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9857 ± 0.0000 | 4.1585 ± 0.0000 | 9.5915 ± 0.0000 | 0.9946 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9879 ± 0.0000 | 6.7644 ± 0.0000 | 9.6267 ± 0.0000 | 0.9023 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.9076 ± 0.0000 | 51.4323 ± 0.0000 | 55.8578 ± 0.0000 | 0.9717 ± 0.0000 | 8200 |
| mp-BRKGA | 0.8508 ± 0.0000 | 84.9629 ± 0.0000 | 151.6687 ± 0.0000 | 1.0002 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8269 ± 0.0000 | 104.9742 ± 0.0000 | 133.6170 ± 0.0000 | 0.8907 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

