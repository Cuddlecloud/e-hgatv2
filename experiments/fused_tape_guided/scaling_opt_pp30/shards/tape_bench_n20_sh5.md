# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8642 ± 0.0000 | 7.2702 ± 0.0000 | 68.0814 ± 0.0000 | 1.1044 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.8321 ± 0.0000 | 63.0376 ± 0.0000 | 58.0056 ± 0.0000 | 0.8736 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.3822 ± 0.0000 | 434.6206 ± 0.0000 | 526.8256 ± 0.0000 | 0.7953 ± 0.0000 | 16400 |
| mp-BRKGA | 0.6637 ± 0.0000 | 617.0570 ± 0.0000 | 145.9236 ± 0.0000 | 1.0909 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.5018 ± 0.0000 | 245.6848 ± 0.0000 | 335.6396 ± 0.0000 | 0.9753 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

