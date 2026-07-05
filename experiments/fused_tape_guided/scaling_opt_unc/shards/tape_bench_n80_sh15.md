# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.6603 ± 0.0000 | 495.2778 ± 0.0000 | 2521.5210 ± 0.0000 | 0.9957 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.8377 ± 0.0000 | 184.2714 ± 0.0000 | 577.3679 ± 0.0000 | 0.9293 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.4302 ± 0.0000 | 1042.9055 ± 0.0000 | 4069.9359 ± 0.0000 | 0.8931 ± 0.0000 | 65600 |
| mp-BRKGA | 0.4844 ± 0.0000 | 1287.3410 ± 0.0000 | 1489.3345 ± 0.0000 | 0.7693 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.3098 ± 0.0000 | 1719.1427 ± 0.0000 | 4542.6986 ± 0.0000 | 0.8335 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

