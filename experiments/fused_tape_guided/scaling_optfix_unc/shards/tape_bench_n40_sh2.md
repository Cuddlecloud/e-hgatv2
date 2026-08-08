# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.4932 ± 0.0000 | 439.4730 ± 0.0000 | 1004.0693 ± 0.0000 | 1.0009 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.6632 ± 0.0000 | 706.8968 ± 0.0000 | 511.7426 ± 0.0000 | 1.0931 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.4905 ± 0.0000 | 1351.8331 ± 0.0000 | 875.7704 ± 0.0000 | 0.9552 ± 0.0000 | 16400 |
| mp-BRKGA | 0.4054 ± 0.0000 | 2394.7993 ± 0.0000 | 643.3594 ± 0.0000 | 0.9969 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.1328 ± 0.0000 | 1973.2026 ± 0.0000 | 1881.6014 ± 0.0000 | 0.9987 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

