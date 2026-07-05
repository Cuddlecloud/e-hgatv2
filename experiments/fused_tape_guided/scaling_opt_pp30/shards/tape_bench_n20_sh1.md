# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8218 ± 0.0000 | 90.1847 ± 0.0000 | 126.1601 ± 0.0000 | 0.9409 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.8880 ± 0.0000 | 44.3680 ± 0.0000 | 68.8550 ± 0.0000 | 0.8986 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.5689 ± 0.0000 | 572.3955 ± 0.0000 | 340.2070 ± 0.0000 | 0.8669 ± 0.0000 | 16400 |
| mp-BRKGA | 0.4741 ± 0.0000 | 611.4940 ± 0.0000 | 501.8245 ± 0.0000 | 1.0744 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.6494 ± 0.0000 | 361.0421 ± 0.0000 | 253.5159 ± 0.0000 | 0.8069 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

