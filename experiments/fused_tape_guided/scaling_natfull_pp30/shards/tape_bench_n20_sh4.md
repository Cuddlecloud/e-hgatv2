# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8618 ± 0.0000 | 0.0000 ± 0.0000 | 57.0466 ± 0.0000 | 0.8822 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7253 ± 0.0000 | 458.3478 ± 0.0000 | 205.5198 ± 0.0000 | 1.0057 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.4299 ± 0.0000 | 792.3396 ± 0.0000 | 528.5986 ± 0.0000 | 0.7940 ± 0.0000 | 16400 |
| mp-BRKGA | 0.8467 ± 0.0000 | 825.2749 ± 0.0000 | 165.9681 ± 0.0000 | 1.0221 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.7500 ± 0.0000 | 352.1210 ± 0.0000 | 251.0245 ± 0.0000 | 0.7618 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

