# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9721 ± 0.0000 | 36.0734 ± 0.0000 | 6.8129 ± 0.0000 | 0.9413 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.8910 ± 0.0000 | 28.8407 ± 0.0000 | 46.0004 ± 0.0000 | 0.9816 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.8717 ± 0.0000 | 43.5716 ± 0.0000 | 47.4412 ± 0.0000 | 0.9095 ± 0.0000 | 8200 |
| mp-BRKGA | 0.6637 ± 0.0000 | 397.6392 ± 0.0000 | 141.0060 ± 0.0000 | 0.9315 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8160 ± 0.0000 | 72.2266 ± 0.0000 | 59.2424 ± 0.0000 | 0.8753 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

