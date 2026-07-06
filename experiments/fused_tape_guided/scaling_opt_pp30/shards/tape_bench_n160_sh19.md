# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9988 ± 0.0000 | 0.0000 ± 0.0000 | 1.4591 ± 0.0000 | 0.8764 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.5855 ± 0.0000 | 925.1104 ± 0.0000 | 841.3929 ± 0.0000 | 1.0676 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0500 ± 0.0000 | 2348.2054 ± 0.0000 | 5019.7907 ± 0.0000 | 0.8836 ± 0.0000 | 131200 |
| mp-BRKGA | 0.0268 ± 0.0000 | 2154.8647 ± 0.0000 | 2084.5534 ± 0.0000 | 0.8402 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0137 ± 0.0000 | 2462.9817 ± 0.0000 | 5319.3953 ± 0.0000 | 0.8931 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

