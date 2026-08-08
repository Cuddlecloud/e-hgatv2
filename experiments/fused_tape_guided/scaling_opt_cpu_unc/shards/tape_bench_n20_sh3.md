# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8878 ± 0.0000 | 103.9000 ± 0.0000 | 144.3535 ± 0.0000 | 0.8376 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.8769 ± 0.0000 | 28.6598 ± 0.0000 | 153.2067 ± 0.0000 | 0.9050 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.8607 ± 0.0000 | 108.7055 ± 0.0000 | 141.1655 ± 0.0000 | 0.8544 ± 0.0000 | 16400 |
| mp-BRKGA | 0.9085 ± 0.0000 | 47.4464 ± 0.0000 | 135.6605 ± 0.0000 | 0.8732 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.8774 ± 0.0000 | 59.0946 ± 0.0000 | 133.2340 ± 0.0000 | 0.9443 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

