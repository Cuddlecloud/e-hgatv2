# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7207 ± 0.0000 | 199.6189 ± 0.0000 | 485.8239 ± 0.0000 | 1.1155 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.8845 ± 0.0000 | 50.9702 ± 0.0000 | 145.0013 ± 0.0000 | 0.8836 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.7720 ± 0.0000 | 51.5000 ± 0.0000 | 370.7438 ± 0.0000 | 0.8224 ± 0.0000 | 16400 |
| mp-BRKGA | 0.7265 ± 0.0000 | 706.8430 ± 0.0000 | 247.1186 ± 0.0000 | 0.9499 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.7137 ± 0.0000 | 211.9710 ± 0.0000 | 362.2245 ± 0.0000 | 0.7070 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

