# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7313 ± 0.0458 | 196.6947 ± 137.5389 | 176.0115 ± 40.4590 | 0.9650 ± 0.1230 | 16400 |
| E-HGATv2-attn | 0.6572 ± 0.1176 | 247.4716 ± 151.0491 | 213.8332 ± 112.8424 | 0.9888 ± 0.1349 | 16400 |
| NSGA-II (random) | 0.5641 ± 0.1914 | 426.2977 ± 407.6471 | 320.1118 ± 227.4155 | 0.8911 ± 0.2024 | 16400 |
| mp-BRKGA | 0.4723 ± 0.1984 | 814.9866 ± 138.2950 | 296.5046 ± 126.7251 | 0.9686 ± 0.0152 | 16400 |
| single-pop BRKGA | 0.7530 ± 0.1716 | 110.3483 ± 174.0508 | 164.0357 ± 83.2545 | 0.8629 ± 0.1178 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

