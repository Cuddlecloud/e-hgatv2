# Faithful-guidance study -- toy:40 (N=40, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8767 ± 0.0000 | 147.7885 ± 0.0000 | 141.4211 ± 0.0000 | 1.0799 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.9028 ± 0.0000 | 47.5635 ± 0.0000 | 101.5656 ± 0.0000 | 0.8926 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.5050 ± 0.0000 | 564.8811 ± 0.0000 | 1541.1280 ± 0.0000 | 0.8945 ± 0.0000 | 32800 |
| mp-BRKGA | 0.7808 ± 0.0000 | 440.7273 ± 0.0000 | 358.7247 ± 0.0000 | 1.0896 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.4750 ± 0.0000 | 611.7927 ± 0.0000 | 1288.2502 ± 0.0000 | 0.7858 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.633 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.902** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 75.981. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

