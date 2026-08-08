# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7478 ± 0.0000 | 324.3537 ± 0.0000 | 295.3920 ± 0.0000 | 0.8549 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.5941 ± 0.0000 | 413.5375 ± 0.0000 | 567.4054 ± 0.0000 | 0.8914 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.4389 ± 0.0000 | 1025.0050 ± 0.0000 | 885.0249 ± 0.0000 | 0.8584 ± 0.0000 | 16400 |
| mp-BRKGA | 0.5594 ± 0.0000 | 2180.5612 ± 0.0000 | 393.7687 ± 0.0000 | 0.9907 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.3018 ± 0.0000 | 1279.0461 ± 0.0000 | 1181.8075 ± 0.0000 | 0.8422 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

