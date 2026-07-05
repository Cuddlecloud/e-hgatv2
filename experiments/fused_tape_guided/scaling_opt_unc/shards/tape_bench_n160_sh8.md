# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.6564 ± 0.0000 | 1290.0650 ± 0.0000 | 962.2810 ± 0.0000 | 0.9323 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.8348 ± 0.0000 | 325.0620 ± 0.0000 | 318.9611 ± 0.0000 | 0.8362 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0000 ± 0.0000 | 4274.6388 ± 0.0000 | 6172.3543 ± 0.0000 | 0.8527 ± 0.0000 | 131200 |
| mp-BRKGA | 0.0039 ± 0.0000 | 6164.0370 ± 0.0000 | 4280.9050 ± 0.0000 | 0.7913 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0000 ± 0.0000 | 5484.1876 ± 0.0000 | 5775.1906 ± 0.0000 | 0.9085 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

