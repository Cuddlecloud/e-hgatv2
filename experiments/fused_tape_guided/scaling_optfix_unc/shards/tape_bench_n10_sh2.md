# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9304 ± 0.0000 | 57.9620 ± 0.0000 | 52.8952 ± 0.0000 | 0.9267 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.9522 ± 0.0000 | 19.1656 ± 0.0000 | 37.5604 ± 0.0000 | 0.8833 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.8472 ± 0.0000 | 80.3061 ± 0.0000 | 87.5741 ± 0.0000 | 0.7948 ± 0.0000 | 16400 |
| mp-BRKGA | 0.8405 ± 0.0000 | 155.6383 ± 0.0000 | 80.1624 ± 0.0000 | 0.9301 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.8914 ± 0.0000 | 48.0766 ± 0.0000 | 77.1860 ± 0.0000 | 0.9377 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

