# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7079 ± 0.0000 | 873.2372 ± 0.0000 | 2880.0256 ± 0.0000 | 0.8895 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7326 ± 0.0000 | 526.8379 ± 0.0000 | 2588.6135 ± 0.0000 | 0.9036 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.5473 ± 0.0000 | 896.4436 ± 0.0000 | 5048.0156 ± 0.0000 | 0.9219 ± 0.0000 | 16400 |
| mp-BRKGA | 0.8654 ± 0.0000 | 214.6443 ± 0.0000 | 455.4621 ± 0.0000 | 0.7721 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.4229 ± 0.0000 | 1877.0356 ± 0.0000 | 5573.4729 ± 0.0000 | 0.9184 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

