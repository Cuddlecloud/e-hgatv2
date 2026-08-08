# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8172 ± 0.0000 | 20.7899 ± 0.0000 | 581.4064 ± 0.0000 | 0.9553 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.8455 ± 0.0000 | 64.2545 ± 0.0000 | 430.8745 ± 0.0000 | 0.7392 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.6214 ± 0.0000 | 540.2744 ± 0.0000 | 1357.0496 ± 0.0000 | 0.8048 ± 0.0000 | 65600 |
| mp-BRKGA | 0.8525 ± 0.0000 | 294.7338 ± 0.0000 | 401.5944 ± 0.0000 | 0.6802 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.5320 ± 0.0000 | 844.5854 ± 0.0000 | 1727.6764 ± 0.0000 | 0.8827 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

