# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9459 ± 0.0000 | 41.4855 ± 0.0000 | 47.0654 ± 0.0000 | 1.1815 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.8594 ± 0.0000 | 86.1787 ± 0.0000 | 108.3583 ± 0.0000 | 1.0471 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.6823 ± 0.0000 | 277.2294 ± 0.0000 | 360.0583 ± 0.0000 | 0.9597 ± 0.0000 | 16400 |
| mp-BRKGA | 0.7626 ± 0.0000 | 162.3557 ± 0.0000 | 189.2259 ± 0.0000 | 1.2262 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.7843 ± 0.0000 | 151.8656 ± 0.0000 | 202.6312 ± 0.0000 | 0.8219 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

