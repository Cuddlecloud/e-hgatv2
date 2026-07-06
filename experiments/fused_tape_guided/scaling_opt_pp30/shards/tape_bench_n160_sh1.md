# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7719 ± 0.0000 | 433.7238 ± 0.0000 | 695.6925 ± 0.0000 | 0.8650 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.8426 ± 0.0000 | 221.6085 ± 0.0000 | 261.6141 ± 0.0000 | 0.8726 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0848 ± 0.0000 | 2300.3286 ± 0.0000 | 4507.4319 ± 0.0000 | 0.8717 ± 0.0000 | 131200 |
| mp-BRKGA | 0.1918 ± 0.0000 | 2301.0533 ± 0.0000 | 1696.0828 ± 0.0000 | 0.5893 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0736 ± 0.0000 | 2605.0845 ± 0.0000 | 5498.2957 ± 0.0000 | 0.8806 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

