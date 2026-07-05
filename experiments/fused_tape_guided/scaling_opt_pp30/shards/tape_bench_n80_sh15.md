# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8098 ± 0.0000 | 92.5109 ± 0.0000 | 863.4849 ± 0.0000 | 0.8474 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.6949 ± 0.0000 | 471.9517 ± 0.0000 | 812.9989 ± 0.0000 | 0.8228 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.2594 ± 0.0000 | 1125.3219 ± 0.0000 | 3594.4893 ± 0.0000 | 0.8851 ± 0.0000 | 65600 |
| mp-BRKGA | 0.4984 ± 0.0000 | 876.8943 ± 0.0000 | 1279.6687 ± 0.0000 | 0.8214 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.2466 ± 0.0000 | 1387.3221 ± 0.0000 | 3427.5656 ± 0.0000 | 0.8943 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

