# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8589 ± 0.0000 | 16.1325 ± 0.0000 | 151.4012 ± 0.0000 | 0.9196 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9826 ± 0.0000 | 5.2712 ± 0.0000 | 7.5010 ± 0.0000 | 1.0079 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.9424 ± 0.0000 | 14.3031 ± 0.0000 | 48.1233 ± 0.0000 | 0.9181 ± 0.0000 | 8200 |
| mp-BRKGA | 0.7384 ± 0.0000 | 233.4490 ± 0.0000 | 137.9884 ± 0.0000 | 0.9321 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.7018 ± 0.0000 | 74.0289 ± 0.0000 | 268.7213 ± 0.0000 | 0.8835 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

