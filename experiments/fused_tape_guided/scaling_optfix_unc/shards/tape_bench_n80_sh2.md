# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8410 ± 0.0000 | 87.8705 ± 0.0000 | 1237.3816 ± 0.0000 | 0.8490 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.8097 ± 0.0000 | 181.7516 ± 0.0000 | 1513.0899 ± 0.0000 | 1.0123 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.6421 ± 0.0000 | 784.2589 ± 0.0000 | 2320.4142 ± 0.0000 | 0.9021 ± 0.0000 | 16400 |
| mp-BRKGA | 0.8390 ± 0.0000 | 582.1805 ± 0.0000 | 615.5982 ± 0.0000 | 0.9289 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.5596 ± 0.0000 | 994.5570 ± 0.0000 | 3220.8495 ± 0.0000 | 0.8912 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

