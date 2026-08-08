# Faithful-guidance study -- toy:20 (N=20, coupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8197 ± 0.1340 | 138.6219 ± 114.2217 | 152.2806 ± 139.6383 | 1.0351 ± 0.1311 | 16400 |
| E-HGATv2-attn | 0.8157 ± 0.1042 | 129.7076 ± 35.7522 | 168.9871 ± 137.9091 | 0.9656 ± 0.1656 | 16400 |
| NSGA-II (random) | 0.6419 ± 0.0975 | 283.4287 ± 101.5598 | 409.3789 ± 180.8053 | 0.9107 ± 0.1649 | 16400 |
| mp-BRKGA | 0.7329 ± 0.1222 | 370.7077 ± 327.9503 | 200.2428 ± 102.4140 | 1.0580 ± 0.1933 | 16400 |
| single-pop BRKGA | 0.7642 ± 0.2246 | 191.0266 ± 229.6479 | 194.1736 ± 235.2391 | 0.9096 ± 0.1609 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

