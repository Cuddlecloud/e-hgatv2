# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7431 ± 0.0000 | 300.5860 ± 0.0000 | 1400.7917 ± 0.0000 | 0.8950 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.9069 ± 0.0000 | 133.5139 ± 0.0000 | 534.9615 ± 0.0000 | 1.0530 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.5561 ± 0.0000 | 760.4805 ± 0.0000 | 2157.0277 ± 0.0000 | 0.8493 ± 0.0000 | 65600 |
| mp-BRKGA | 0.7785 ± 0.0000 | 570.7329 ± 0.0000 | 355.3982 ± 0.0000 | 0.9332 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.4938 ± 0.0000 | 874.8000 ± 0.0000 | 2468.6742 ± 0.0000 | 0.8295 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

