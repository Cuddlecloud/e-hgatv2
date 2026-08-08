# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7808 ± 0.0000 | 132.2514 ± 0.0000 | 228.6537 ± 0.0000 | 0.9516 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.9114 ± 0.0000 | 203.1528 ± 0.0000 | 92.0069 ± 0.0000 | 0.9656 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.8563 ± 0.0000 | 48.0031 ± 0.0000 | 124.2653 ± 0.0000 | 0.8254 ± 0.0000 | 16400 |
| mp-BRKGA | 0.9345 ± 0.0000 | 1149.6136 ± 0.0000 | 65.2347 ± 0.0000 | 1.1050 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.8022 ± 0.0000 | 159.9581 ± 0.0000 | 197.8624 ± 0.0000 | 0.8931 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

