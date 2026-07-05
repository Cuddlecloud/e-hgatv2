# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.6514 ± 0.0000 | 970.7031 ± 0.0000 | 935.7081 ± 0.0000 | 1.0497 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.6111 ± 0.0000 | 1065.6906 ± 0.0000 | 896.5879 ± 0.0000 | 0.9133 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.1349 ± 0.0000 | 2982.1306 ± 0.0000 | 3723.3325 ± 0.0000 | 0.8334 ± 0.0000 | 65600 |
| mp-BRKGA | 0.3831 ± 0.0000 | 1673.1450 ± 0.0000 | 1442.4450 ± 0.0000 | 0.8856 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.0236 ± 0.0000 | 3724.2282 ± 0.0000 | 5373.3717 ± 0.0000 | 0.8076 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

