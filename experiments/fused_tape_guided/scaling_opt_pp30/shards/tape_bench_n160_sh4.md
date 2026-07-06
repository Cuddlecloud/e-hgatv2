# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9298 ± 0.0000 | 75.7458 ± 0.0000 | 419.2250 ± 0.0000 | 0.8033 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.8205 ± 0.0000 | 341.9622 ± 0.0000 | 360.2076 ± 0.0000 | 0.9015 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.1942 ± 0.0000 | 3071.3886 ± 0.0000 | 6656.0158 ± 0.0000 | 1.0057 ± 0.0000 | 131200 |
| mp-BRKGA | 0.2419 ± 0.0000 | 2582.5499 ± 0.0000 | 4485.6560 ± 0.0000 | 0.7857 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.1558 ± 0.0000 | 2825.2001 ± 0.0000 | 7184.2908 ± 0.0000 | 0.8009 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

