# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9536 ± 0.0000 | 80.9229 ± 0.0000 | 41.6477 ± 0.0000 | 0.8952 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9143 ± 0.0000 | 14.2159 ± 0.0000 | 59.3518 ± 0.0000 | 0.9794 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.7628 ± 0.0000 | 185.8382 ± 0.0000 | 143.1973 ± 0.0000 | 0.8856 ± 0.0000 | 8200 |
| mp-BRKGA | 0.7559 ± 0.0000 | 311.5518 ± 0.0000 | 100.1585 ± 0.0000 | 0.8748 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8732 ± 0.0000 | 41.4266 ± 0.0000 | 62.3050 ± 0.0000 | 0.8771 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

