# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9184 ± 0.0000 | 32.6711 ± 0.0000 | 28.5509 ± 0.0000 | 1.2166 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9408 ± 0.0000 | 25.7034 ± 0.0000 | 22.7756 ± 0.0000 | 0.9846 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.8016 ± 0.0000 | 121.4964 ± 0.0000 | 50.9478 ± 0.0000 | 0.9584 ± 0.0000 | 8200 |
| mp-BRKGA | 0.5987 ± 0.0000 | 109.4367 ± 0.0000 | 134.3309 ± 0.0000 | 0.7279 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.9308 ± 0.0000 | 6.2616 ± 0.0000 | 10.8061 ± 0.0000 | 0.9149 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

