# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9383 ± 0.0000 | 26.5877 ± 0.0000 | 26.5876 ± 0.0000 | 0.8200 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.8816 ± 0.0000 | 27.6638 ± 0.0000 | 36.0666 ± 0.0000 | 1.2274 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.8490 ± 0.0000 | 270.7292 ± 0.0000 | 72.1751 ± 0.0000 | 1.0075 ± 0.0000 | 8200 |
| mp-BRKGA | 0.6781 ± 0.0000 | 187.7817 ± 0.0000 | 128.4943 ± 0.0000 | 0.8755 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.7057 ± 0.0000 | 83.3718 ± 0.0000 | 163.9900 ± 0.0000 | 0.9783 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

