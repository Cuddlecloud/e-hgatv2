# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8430 ± 0.0000 | 56.5215 ± 0.0000 | 106.7361 ± 0.0000 | 1.0008 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.9168 ± 0.0000 | 75.2760 ± 0.0000 | 76.4297 ± 0.0000 | 1.0269 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.6238 ± 0.0000 | 306.3402 ± 0.0000 | 383.2965 ± 0.0000 | 0.8445 ± 0.0000 | 16400 |
| mp-BRKGA | 0.6893 ± 0.0000 | 413.6621 ± 0.0000 | 276.9597 ± 0.0000 | 1.0276 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.6119 ± 0.0000 | 273.6241 ± 0.0000 | 386.3384 ± 0.0000 | 0.8648 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

