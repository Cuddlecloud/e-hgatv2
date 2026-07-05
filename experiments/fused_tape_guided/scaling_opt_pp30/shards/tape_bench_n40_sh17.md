# Faithful-guidance study -- toy:40 (N=40, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9789 ± 0.0000 | 5.6544 ± 0.0000 | 35.6042 ± 0.0000 | 0.9248 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.8130 ± 0.0000 | 256.9464 ± 0.0000 | 364.6980 ± 0.0000 | 0.8911 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.4271 ± 0.0000 | 649.4334 ± 0.0000 | 1769.0336 ± 0.0000 | 0.9377 ± 0.0000 | 32800 |
| mp-BRKGA | 0.7879 ± 0.0000 | 233.4736 ± 0.0000 | 325.6320 ± 0.0000 | 0.8463 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.5281 ± 0.0000 | 523.4173 ± 0.0000 | 1439.0194 ± 0.0000 | 0.8356 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.633 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.902** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 75.981. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

