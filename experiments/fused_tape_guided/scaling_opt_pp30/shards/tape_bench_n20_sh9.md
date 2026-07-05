# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9046 ± 0.0000 | 60.6148 ± 0.0000 | 68.6801 ± 0.0000 | 1.0139 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7642 ± 0.0000 | 352.4212 ± 0.0000 | 173.7083 ± 0.0000 | 1.1843 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.4314 ± 0.0000 | 567.3462 ± 0.0000 | 550.9850 ± 0.0000 | 1.0128 ± 0.0000 | 16400 |
| mp-BRKGA | 0.7150 ± 0.0000 | 814.3005 ± 0.0000 | 194.7376 ± 0.0000 | 0.9996 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.6061 ± 0.0000 | 206.5382 ± 0.0000 | 352.6033 ± 0.0000 | 0.8331 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

