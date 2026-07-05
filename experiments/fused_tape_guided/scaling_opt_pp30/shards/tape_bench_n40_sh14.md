# Faithful-guidance study -- toy:40 (N=40, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8709 ± 0.0000 | 191.9720 ± 0.0000 | 231.2371 ± 0.0000 | 0.8632 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.9236 ± 0.0000 | 65.3125 ± 0.0000 | 99.1575 ± 0.0000 | 0.8390 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.4440 ± 0.0000 | 677.3190 ± 0.0000 | 1649.2590 ± 0.0000 | 0.8474 ± 0.0000 | 32800 |
| mp-BRKGA | 0.8219 ± 0.0000 | 383.2236 ± 0.0000 | 237.4132 ± 0.0000 | 1.0536 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.6358 ± 0.0000 | 377.1157 ± 0.0000 | 766.1375 ± 0.0000 | 0.8495 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.633 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.902** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 75.981. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

