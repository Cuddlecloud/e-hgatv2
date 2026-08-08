# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8975 ± 0.0000 | 28.6845 ± 0.0000 | 149.2063 ± 0.0000 | 0.8009 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.8919 ± 0.0000 | 274.4692 ± 0.0000 | 170.3976 ± 0.0000 | 0.7269 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.6266 ± 0.0000 | 494.0947 ± 0.0000 | 854.4641 ± 0.0000 | 0.8038 ± 0.0000 | 65600 |
| mp-BRKGA | 0.8577 ± 0.0000 | 351.1503 ± 0.0000 | 291.5347 ± 0.0000 | 0.4542 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.5142 ± 0.0000 | 1069.0131 ± 0.0000 | 1226.1270 ± 0.0000 | 0.7338 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

