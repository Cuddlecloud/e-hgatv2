# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.4853 ± 0.0000 | 891.2767 ± 0.0000 | 801.7120 ± 0.0000 | 0.8643 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7090 ± 0.0000 | 550.1835 ± 0.0000 | 502.7559 ± 0.0000 | 0.8199 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.1287 ± 0.0000 | 1546.7881 ± 0.0000 | 1918.7790 ± 0.0000 | 0.8304 ± 0.0000 | 16400 |
| mp-BRKGA | 0.6376 ± 0.0000 | 998.5562 ± 0.0000 | 322.3692 ± 0.0000 | 0.8793 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.1740 ± 0.0000 | 1963.9338 ± 0.0000 | 1783.9728 ± 0.0000 | 0.8812 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

