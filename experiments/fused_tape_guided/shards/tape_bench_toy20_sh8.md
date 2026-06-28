# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9120 ± 0.1901 | 70.4243 ± 85.4380 | 97.0782 ± 130.8752 | 0.8309 ± 0.0544 | 16400 |
| E-HGATv2-attn | 0.9669 ± 0.1435 | 69.7222 ± 63.4001 | 49.7750 ± 57.9766 | 0.9001 ± 0.1372 | 16400 |
| NSGA-II (random) | 0.6796 ± 0.1418 | 357.6848 ± 403.2298 | 287.2819 ± 180.0112 | 0.8332 ± 0.2057 | 16400 |
| mp-BRKGA | 0.8502 ± 0.1903 | 625.0336 ± 246.7205 | 144.2423 ± 99.6097 | 1.0042 ± 0.0897 | 16400 |
| single-pop BRKGA | 0.7981 ± 0.1959 | 221.8464 ± 207.1785 | 157.1871 ± 164.6258 | 0.8154 ± 0.1955 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

