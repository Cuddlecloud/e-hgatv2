# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9003 ± 0.0000 | 109.1108 ± 0.0000 | 86.9533 ± 0.0000 | 0.9242 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9751 ± 0.0000 | 10.1335 ± 0.0000 | 7.3685 ± 0.0000 | 0.8625 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.7917 ± 0.0000 | 79.5427 ± 0.0000 | 130.5716 ± 0.0000 | 0.9288 ± 0.0000 | 8200 |
| mp-BRKGA | 0.7718 ± 0.0000 | 124.2540 ± 0.0000 | 150.2245 ± 0.0000 | 0.7035 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.7870 ± 0.0000 | 98.4095 ± 0.0000 | 145.1531 ± 0.0000 | 0.8827 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

