# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7760 ± 0.0000 | 203.0330 ± 0.0000 | 1128.4024 ± 0.0000 | 0.8949 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7711 ± 0.0000 | 114.0767 ± 0.0000 | 1301.7670 ± 0.0000 | 0.9091 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.5713 ± 0.0000 | 338.9676 ± 0.0000 | 2378.3130 ± 0.0000 | 0.8155 ± 0.0000 | 16400 |
| mp-BRKGA | 0.8805 ± 0.0000 | 397.8489 ± 0.0000 | 360.6573 ± 0.0000 | 0.8782 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.5352 ± 0.0000 | 1241.6855 ± 0.0000 | 2317.7427 ± 0.0000 | 0.9095 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

