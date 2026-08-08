# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9838 ± 0.0000 | 9.2597 ± 0.0000 | 15.4953 ± 0.0000 | 0.7757 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7493 ± 0.0000 | 287.7000 ± 0.0000 | 204.4788 ± 0.0000 | 1.1464 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.6404 ± 0.0000 | 397.1599 ± 0.0000 | 262.0540 ± 0.0000 | 0.8365 ± 0.0000 | 16400 |
| mp-BRKGA | 0.7470 ± 0.0000 | 284.1999 ± 0.0000 | 131.2719 ± 0.0000 | 1.0637 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.6649 ± 0.0000 | 205.3918 ± 0.0000 | 267.0301 ± 0.0000 | 0.9177 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

