# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9268 ± 0.0000 | 0.4994 ± 0.0000 | 77.0657 ± 0.0000 | 1.3198 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7365 ± 0.0000 | 122.7280 ± 0.0000 | 163.9076 ± 0.0000 | 0.8766 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.5965 ± 0.0000 | 333.2503 ± 0.0000 | 373.3311 ± 0.0000 | 0.8455 ± 0.0000 | 16400 |
| mp-BRKGA | 0.5248 ± 0.0000 | 567.5244 ± 0.0000 | 511.0126 ± 0.0000 | 1.0796 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.6447 ± 0.0000 | 232.9872 ± 0.0000 | 263.9422 ± 0.0000 | 0.7728 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

