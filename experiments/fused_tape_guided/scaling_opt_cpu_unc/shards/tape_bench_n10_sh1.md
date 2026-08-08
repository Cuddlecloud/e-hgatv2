# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9866 ± 0.0000 | 7.6351 ± 0.0000 | 9.6269 ± 0.0000 | 0.8948 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9242 ± 0.0000 | 18.1043 ± 0.0000 | 72.0832 ± 0.0000 | 0.8261 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.8380 ± 0.0000 | 86.1011 ± 0.0000 | 138.5764 ± 0.0000 | 0.8644 ± 0.0000 | 8200 |
| mp-BRKGA | 0.8488 ± 0.0000 | 55.9580 ± 0.0000 | 89.2731 ± 0.0000 | 0.8522 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8745 ± 0.0000 | 46.1540 ± 0.0000 | 80.8655 ± 0.0000 | 0.8695 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

