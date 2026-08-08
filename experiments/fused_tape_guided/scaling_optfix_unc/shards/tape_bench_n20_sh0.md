# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9289 ± 0.0000 | 70.9536 ± 0.0000 | 51.2341 ± 0.0000 | 1.0516 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.8862 ± 0.0000 | 81.6780 ± 0.0000 | 131.9846 ± 0.0000 | 0.8618 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.6707 ± 0.0000 | 211.7245 ± 0.0000 | 382.8257 ± 0.0000 | 0.8500 ± 0.0000 | 16400 |
| mp-BRKGA | 0.8287 ± 0.0000 | 402.6875 ± 0.0000 | 111.5919 ± 0.0000 | 0.9401 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.6606 ± 0.0000 | 253.6622 ± 0.0000 | 428.9486 ± 0.0000 | 0.8948 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

