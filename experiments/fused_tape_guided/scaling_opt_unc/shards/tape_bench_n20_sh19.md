# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7657 ± 0.0000 | 177.1562 ± 0.0000 | 213.9786 ± 0.0000 | 1.0042 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7799 ± 0.0000 | 112.6404 ± 0.0000 | 134.0225 ± 0.0000 | 1.0218 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.5287 ± 0.0000 | 506.0131 ± 0.0000 | 541.2817 ± 0.0000 | 0.8051 ± 0.0000 | 16400 |
| mp-BRKGA | 0.6711 ± 0.0000 | 406.1733 ± 0.0000 | 194.0153 ± 0.0000 | 0.9045 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.8101 ± 0.0000 | 74.3901 ± 0.0000 | 143.9080 ± 0.0000 | 1.0338 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

