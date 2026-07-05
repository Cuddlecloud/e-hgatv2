# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8938 ± 0.0000 | 11.2294 ± 0.0000 | 64.1419 ± 0.0000 | 0.8289 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.8466 ± 0.0000 | 82.2500 ± 0.0000 | 86.3851 ± 0.0000 | 1.0328 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.8623 ± 0.0000 | 78.9422 ± 0.0000 | 85.0771 ± 0.0000 | 0.9176 ± 0.0000 | 8200 |
| mp-BRKGA | 0.9087 ± 0.0000 | 40.6909 ± 0.0000 | 50.4901 ± 0.0000 | 0.7933 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8380 ± 0.0000 | 47.7299 ± 0.0000 | 89.9231 ± 0.0000 | 1.0467 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

