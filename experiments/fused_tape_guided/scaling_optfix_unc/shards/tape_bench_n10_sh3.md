# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9614 ± 0.0000 | 23.3627 ± 0.0000 | 17.4377 ± 0.0000 | 1.0267 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.9599 ± 0.0000 | 11.8572 ± 0.0000 | 16.3439 ± 0.0000 | 0.7924 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.8694 ± 0.0000 | 51.7386 ± 0.0000 | 89.9038 ± 0.0000 | 0.9348 ± 0.0000 | 16400 |
| mp-BRKGA | 0.7365 ± 0.0000 | 275.6212 ± 0.0000 | 152.8317 ± 0.0000 | 0.8721 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.9402 ± 0.0000 | 37.0855 ± 0.0000 | 28.7742 ± 0.0000 | 0.9359 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

