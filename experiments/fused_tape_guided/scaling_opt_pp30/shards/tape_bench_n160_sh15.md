# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8070 ± 0.0000 | 463.2577 ± 0.0000 | 1020.4904 ± 0.0000 | 0.9367 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.8558 ± 0.0000 | 528.2995 ± 0.0000 | 576.5769 ± 0.0000 | 0.8734 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.3051 ± 0.0000 | 2136.3321 ± 0.0000 | 4642.4062 ± 0.0000 | 0.8572 ± 0.0000 | 131200 |
| mp-BRKGA | 0.3926 ± 0.0000 | 2419.7379 ± 0.0000 | 3322.5834 ± 0.0000 | 0.6758 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.3014 ± 0.0000 | 2273.4062 ± 0.0000 | 5043.2199 ± 0.0000 | 0.8849 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

