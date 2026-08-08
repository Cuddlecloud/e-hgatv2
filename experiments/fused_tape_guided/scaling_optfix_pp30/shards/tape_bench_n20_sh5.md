# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8314 ± 0.0000 | 188.5376 ± 0.0000 | 177.9032 ± 0.0000 | 1.0588 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.6511 ± 0.0000 | 224.6356 ± 0.0000 | 254.6399 ± 0.0000 | 1.0188 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.5787 ± 0.0000 | 369.7792 ± 0.0000 | 480.8794 ± 0.0000 | 0.8295 ± 0.0000 | 16400 |
| mp-BRKGA | 0.7727 ± 0.0000 | 310.6108 ± 0.0000 | 82.0307 ± 0.0000 | 1.1085 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.6914 ± 0.0000 | 135.1262 ± 0.0000 | 364.7128 ± 0.0000 | 0.9690 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

