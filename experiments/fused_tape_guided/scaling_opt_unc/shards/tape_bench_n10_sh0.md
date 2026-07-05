# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8786 ± 0.0000 | 84.0619 ± 0.0000 | 70.5888 ± 0.0000 | 1.1129 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.8465 ± 0.0000 | 116.7107 ± 0.0000 | 85.5007 ± 0.0000 | 0.8509 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.8057 ± 0.0000 | 100.8105 ± 0.0000 | 110.2695 ± 0.0000 | 0.9950 ± 0.0000 | 8200 |
| mp-BRKGA | 0.8121 ± 0.0000 | 141.1461 ± 0.0000 | 97.7574 ± 0.0000 | 0.7553 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.9093 ± 0.0000 | 31.1827 ± 0.0000 | 47.9335 ± 0.0000 | 0.8577 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

