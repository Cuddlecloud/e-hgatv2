# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9008 ± 0.0000 | 173.1594 ± 0.0000 | 192.2510 ± 0.0000 | 0.8602 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.8759 ± 0.0000 | 49.5263 ± 0.0000 | 143.7964 ± 0.0000 | 0.8732 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0136 ± 0.0000 | 2213.5438 ± 0.0000 | 4210.1504 ± 0.0000 | 0.9172 ± 0.0000 | 131200 |
| mp-BRKGA | 0.0120 ± 0.0000 | 2750.5361 ± 0.0000 | 2827.3581 ± 0.0000 | 0.9193 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0032 ± 0.0000 | 2620.2742 ± 0.0000 | 4156.0397 ± 0.0000 | 0.7566 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

