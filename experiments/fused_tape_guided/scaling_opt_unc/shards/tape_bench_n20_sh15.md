# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7750 ± 0.0000 | 96.9120 ± 0.0000 | 213.4698 ± 0.0000 | 1.1868 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7382 ± 0.0000 | 142.1778 ± 0.0000 | 134.9348 ± 0.0000 | 0.9383 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.4983 ± 0.0000 | 476.6027 ± 0.0000 | 717.0011 ± 0.0000 | 0.9544 ± 0.0000 | 16400 |
| mp-BRKGA | 0.4595 ± 0.0000 | 694.1917 ± 0.0000 | 376.3362 ± 0.0000 | 0.9780 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.8049 ± 0.0000 | 81.8845 ± 0.0000 | 193.4974 ± 0.0000 | 0.8771 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

