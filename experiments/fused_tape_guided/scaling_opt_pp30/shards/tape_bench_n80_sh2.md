# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8240 ± 0.0000 | 100.9972 ± 0.0000 | 775.3099 ± 0.0000 | 0.6611 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.7328 ± 0.0000 | 385.0078 ± 0.0000 | 735.5018 ± 0.0000 | 0.9325 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.1942 ± 0.0000 | 1777.6768 ± 0.0000 | 3321.2883 ± 0.0000 | 1.0241 ± 0.0000 | 65600 |
| mp-BRKGA | 0.4191 ± 0.0000 | 2052.5940 ± 0.0000 | 1225.8662 ± 0.0000 | 0.9982 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.1264 ± 0.0000 | 1863.4811 ± 0.0000 | 3840.2596 ± 0.0000 | 0.7841 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

