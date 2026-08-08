# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8586 ± 0.0000 | 105.2521 ± 0.0000 | 96.8065 ± 0.0000 | 0.8931 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9856 ± 0.0000 | 46.5094 ± 0.0000 | 3.1034 ± 0.0000 | 0.8796 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.7253 ± 0.0000 | 171.6195 ± 0.0000 | 157.7953 ± 0.0000 | 0.9427 ± 0.0000 | 8200 |
| mp-BRKGA | 0.7076 ± 0.0000 | 167.9608 ± 0.0000 | 158.6363 ± 0.0000 | 0.7671 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.7088 ± 0.0000 | 140.0451 ± 0.0000 | 167.1046 ± 0.0000 | 0.9058 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

