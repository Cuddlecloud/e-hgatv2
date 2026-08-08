# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9090 ± 0.0000 | 195.5679 ± 0.0000 | 249.9368 ± 0.0000 | 0.8312 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.9896 ± 0.0000 | 11.3291 ± 0.0000 | 28.4078 ± 0.0000 | 0.8537 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.6967 ± 0.0000 | 949.2800 ± 0.0000 | 831.2761 ± 0.0000 | 0.9270 ± 0.0000 | 65600 |
| mp-BRKGA | 0.6721 ± 0.0000 | 1011.8885 ± 0.0000 | 705.6862 ± 0.0000 | 0.7606 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.4464 ± 0.0000 | 1604.5984 ± 0.0000 | 2081.4815 ± 0.0000 | 0.8793 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

