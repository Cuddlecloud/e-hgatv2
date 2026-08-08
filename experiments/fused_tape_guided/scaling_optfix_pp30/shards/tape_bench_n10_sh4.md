# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9609 ± 0.0000 | 10.7435 ± 0.0000 | 36.2417 ± 0.0000 | 1.1156 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.9515 ± 0.0000 | 33.3784 ± 0.0000 | 32.0315 ± 0.0000 | 1.0817 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.8806 ± 0.0000 | 73.2774 ± 0.0000 | 77.5668 ± 0.0000 | 0.9879 ± 0.0000 | 16400 |
| mp-BRKGA | 0.7744 ± 0.0000 | 158.3315 ± 0.0000 | 119.6981 ± 0.0000 | 0.9512 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.9426 ± 0.0000 | 23.0374 ± 0.0000 | 31.3969 ± 0.0000 | 1.0724 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

