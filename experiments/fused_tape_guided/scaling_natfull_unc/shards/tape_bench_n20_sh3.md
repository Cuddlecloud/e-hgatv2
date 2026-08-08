# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8967 ± 0.0000 | 91.1218 ± 0.0000 | 154.0841 ± 0.0000 | 0.8376 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.8856 ± 0.0000 | 3.8138 ± 0.0000 | 134.9994 ± 0.0000 | 0.9050 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.8693 ± 0.0000 | 97.3322 ± 0.0000 | 129.7248 ± 0.0000 | 0.8544 ± 0.0000 | 16400 |
| mp-BRKGA | 0.9176 ± 0.0000 | 39.6507 ± 0.0000 | 141.5598 ± 0.0000 | 0.8732 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.8862 ± 0.0000 | 46.2445 ± 0.0000 | 123.9189 ± 0.0000 | 0.9443 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

