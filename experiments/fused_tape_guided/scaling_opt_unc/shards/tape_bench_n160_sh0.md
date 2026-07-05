# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.3910 ± 0.0000 | 3292.6523 ± 0.0000 | 1933.0407 ± 0.0000 | 0.8404 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.7510 ± 0.0000 | 452.2911 ± 0.0000 | 403.5273 ± 0.0000 | 0.7997 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0412 ± 0.0000 | 6173.8678 ± 0.0000 | 5125.7700 ± 0.0000 | 0.9664 ± 0.0000 | 131200 |
| mp-BRKGA | 0.0104 ± 0.0000 | 7229.9047 ± 0.0000 | 5581.8639 ± 0.0000 | 0.7805 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0000 ± 0.0000 | 5924.7384 ± 0.0000 | 6532.6131 ± 0.0000 | 0.8565 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

