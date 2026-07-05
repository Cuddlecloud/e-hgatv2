# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9862 ± 0.0000 | 6.8092 ± 0.0000 | 6.8832 ± 0.0000 | 0.9146 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9558 ± 0.0000 | 13.6839 ± 0.0000 | 20.8832 ± 0.0000 | 0.8768 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.8747 ± 0.0000 | 38.2639 ± 0.0000 | 61.8261 ± 0.0000 | 1.0286 ± 0.0000 | 8200 |
| mp-BRKGA | 0.8172 ± 0.0000 | 185.3657 ± 0.0000 | 68.0795 ± 0.0000 | 1.0414 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8139 ± 0.0000 | 72.2946 ± 0.0000 | 98.5824 ± 0.0000 | 0.7220 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

