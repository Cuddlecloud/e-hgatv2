# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8782 ± 0.0000 | 92.1232 ± 0.0000 | 540.4982 ± 0.0000 | 0.7632 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.7635 ± 0.0000 | 360.8694 ± 0.0000 | 691.6790 ± 0.0000 | 0.8281 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.3985 ± 0.0000 | 1382.9298 ± 0.0000 | 1996.9315 ± 0.0000 | 1.0272 ± 0.0000 | 65600 |
| mp-BRKGA | 0.7973 ± 0.0000 | 1184.2487 ± 0.0000 | 269.9647 ± 0.0000 | 0.9980 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.2951 ± 0.0000 | 1466.4354 ± 0.0000 | 2444.5877 ± 0.0000 | 0.7444 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

