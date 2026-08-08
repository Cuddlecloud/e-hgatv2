# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8407 ± 0.0000 | 0.0000 ± 0.0000 | 79.7288 ± 0.0000 | 0.8287 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7926 ± 0.0000 | 290.6024 ± 0.0000 | 173.5292 ± 0.0000 | 0.7859 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.6521 ± 0.0000 | 244.0739 ± 0.0000 | 247.7894 ± 0.0000 | 0.8777 ± 0.0000 | 16400 |
| mp-BRKGA | 0.6648 ± 0.0000 | 1056.8827 ± 0.0000 | 251.7424 ± 0.0000 | 0.8519 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.4499 ± 0.0000 | 1291.4231 ± 0.0000 | 415.9033 ± 0.0000 | 1.0062 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

