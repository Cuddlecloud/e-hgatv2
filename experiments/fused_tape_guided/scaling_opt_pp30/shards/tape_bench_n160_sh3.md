# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9018 ± 0.0000 | 109.5249 ± 0.0000 | 356.3880 ± 0.0000 | 0.8772 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.8359 ± 0.0000 | 51.4906 ± 0.0000 | 214.2098 ± 0.0000 | 0.8154 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.1193 ± 0.0000 | 1815.5582 ± 0.0000 | 4237.9306 ± 0.0000 | 0.9255 ± 0.0000 | 131200 |
| mp-BRKGA | 0.1032 ± 0.0000 | 2611.2743 ± 0.0000 | 3131.9116 ± 0.0000 | 0.8472 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0601 ± 0.0000 | 2297.5288 ± 0.0000 | 5353.0516 ± 0.0000 | 0.8306 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

