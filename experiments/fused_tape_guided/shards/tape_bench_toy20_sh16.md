# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8472 ± 0.0855 | 104.0665 ± 60.0711 | 254.3248 ± 176.6226 | 0.9270 ± 0.1185 | 16400 |
| E-HGATv2-attn | 0.7791 ± 0.0933 | 149.4427 ± 121.5287 | 309.1104 ± 190.2112 | 0.9570 ± 0.0699 | 16400 |
| NSGA-II (random) | 0.7424 ± 0.0995 | 182.8188 ± 83.6093 | 388.8699 ± 225.6739 | 0.8185 ± 0.0551 | 16400 |
| mp-BRKGA | 0.7625 ± 0.0881 | 193.3055 ± 102.1623 | 250.0938 ± 145.6509 | 0.8901 ± 0.0819 | 16400 |
| single-pop BRKGA | 0.7745 ± 0.1550 | 168.3758 ± 203.7109 | 346.9616 ± 196.5710 | 0.8828 ± 0.1585 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

