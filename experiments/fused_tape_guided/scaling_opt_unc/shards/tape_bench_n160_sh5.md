# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.5382 ± 0.0000 | 704.0712 ± 0.0000 | 1720.0684 ± 0.0000 | 0.8333 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.6737 ± 0.0000 | 1068.3288 ± 0.0000 | 620.0504 ± 0.0000 | 0.9979 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0000 ± 0.0000 | 4933.5712 ± 0.0000 | 5758.7695 ± 0.0000 | 0.8874 ± 0.0000 | 131200 |
| mp-BRKGA | 0.0000 ± 0.0000 | 6955.5665 ± 0.0000 | 3702.4393 ± 0.0000 | 0.8776 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0002 ± 0.0000 | 5718.8929 ± 0.0000 | 6253.6031 ± 0.0000 | 0.8894 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

