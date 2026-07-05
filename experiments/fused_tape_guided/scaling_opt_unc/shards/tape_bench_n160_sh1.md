# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7585 ± 0.0000 | 1160.7002 ± 0.0000 | 600.0214 ± 0.0000 | 0.8546 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.7808 ± 0.0000 | 2217.7248 ± 0.0000 | 493.4248 ± 0.0000 | 1.0472 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0000 ± 0.0000 | 4459.7331 ± 0.0000 | 6377.4201 ± 0.0000 | 0.9316 ± 0.0000 | 131200 |
| mp-BRKGA | 0.0415 ± 0.0000 | 5802.6958 ± 0.0000 | 2381.7691 ± 0.0000 | 0.8042 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0000 ± 0.0000 | 5597.7257 ± 0.0000 | 7035.7127 ± 0.0000 | 0.8352 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

