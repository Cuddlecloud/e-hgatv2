# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9662 ± 0.0000 | 19.7487 ± 0.0000 | 15.5008 ± 0.0000 | 0.7768 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.8703 ± 0.0000 | 109.4208 ± 0.0000 | 78.2194 ± 0.0000 | 0.9737 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.7654 ± 0.0000 | 93.7562 ± 0.0000 | 120.4123 ± 0.0000 | 0.7901 ± 0.0000 | 8200 |
| mp-BRKGA | 0.7852 ± 0.0000 | 224.9706 ± 0.0000 | 99.1643 ± 0.0000 | 0.8309 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8494 ± 0.0000 | 56.3081 ± 0.0000 | 59.5015 ± 0.0000 | 0.8509 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

