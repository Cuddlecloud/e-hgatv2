# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9141 ± 0.0000 | 18.3201 ± 0.0000 | 60.8990 ± 0.0000 | 1.2092 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9722 ± 0.0000 | 5.4364 ± 0.0000 | 5.9888 ± 0.0000 | 0.9321 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.8955 ± 0.0000 | 45.2807 ± 0.0000 | 48.2498 ± 0.0000 | 0.9761 ± 0.0000 | 8200 |
| mp-BRKGA | 0.8946 ± 0.0000 | 42.4444 ± 0.0000 | 78.6735 ± 0.0000 | 0.8578 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.7573 ± 0.0000 | 71.9604 ± 0.0000 | 219.3203 ± 0.0000 | 1.0169 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

