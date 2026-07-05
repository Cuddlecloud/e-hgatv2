# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.5347 ± 0.0000 | 1602.9026 ± 0.0000 | 1532.1465 ± 0.0000 | 0.9078 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.6337 ± 0.0000 | 1999.5566 ± 0.0000 | 1051.7960 ± 0.0000 | 0.9422 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.1672 ± 0.0000 | 2309.6011 ± 0.0000 | 3879.1698 ± 0.0000 | 0.9446 ± 0.0000 | 65600 |
| mp-BRKGA | 0.6897 ± 0.0000 | 3117.6027 ± 0.0000 | 795.3035 ± 0.0000 | 0.8557 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.1330 ± 0.0000 | 3528.7610 ± 0.0000 | 4353.3997 ± 0.0000 | 0.8118 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

