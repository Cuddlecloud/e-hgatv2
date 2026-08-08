# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8942 ± 0.0000 | 112.1651 ± 0.0000 | 248.2456 ± 0.0000 | 0.9715 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.9571 ± 0.0000 | 77.8709 ± 0.0000 | 95.1285 ± 0.0000 | 0.9707 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.9207 ± 0.0000 | 35.3961 ± 0.0000 | 156.7105 ± 0.0000 | 0.8985 ± 0.0000 | 16400 |
| mp-BRKGA | 0.9623 ± 0.0000 | 21.9948 ± 0.0000 | 42.9003 ± 0.0000 | 1.1474 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.8956 ± 0.0000 | 91.7174 ± 0.0000 | 235.8320 ± 0.0000 | 0.9124 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

