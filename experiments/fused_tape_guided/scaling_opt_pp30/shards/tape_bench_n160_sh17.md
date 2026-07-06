# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8004 ± 0.0000 | 817.2459 ± 0.0000 | 930.2121 ± 0.0000 | 0.7040 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.7993 ± 0.0000 | 795.6371 ± 0.0000 | 749.3812 ± 0.0000 | 0.8618 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.3506 ± 0.0000 | 1808.0880 ± 0.0000 | 4453.9834 ± 0.0000 | 0.9370 ± 0.0000 | 131200 |
| mp-BRKGA | 0.3738 ± 0.0000 | 2664.4049 ± 0.0000 | 3327.7229 ± 0.0000 | 0.7403 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.2879 ± 0.0000 | 2128.8864 ± 0.0000 | 5003.0112 ± 0.0000 | 0.8403 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

