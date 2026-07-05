# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.5009 ± 0.0000 | 2556.9599 ± 0.0000 | 1633.3589 ± 0.0000 | 0.8831 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.7331 ± 0.0000 | 729.8225 ± 0.0000 | 575.9305 ± 0.0000 | 1.0094 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0000 ± 0.0000 | 5233.1254 ± 0.0000 | 5787.0958 ± 0.0000 | 0.9401 ± 0.0000 | 131200 |
| mp-BRKGA | 0.0004 ± 0.0000 | 6382.1214 ± 0.0000 | 5271.4855 ± 0.0000 | 0.7967 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0000 ± 0.0000 | 6527.7100 ± 0.0000 | 6426.6256 ± 0.0000 | 0.9327 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

