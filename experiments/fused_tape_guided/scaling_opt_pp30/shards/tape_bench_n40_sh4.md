# Faithful-guidance study -- toy:40 (N=40, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8802 ± 0.0000 | 32.5874 ± 0.0000 | 290.4633 ± 0.0000 | 1.0498 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.8465 ± 0.0000 | 216.4677 ± 0.0000 | 302.4872 ± 0.0000 | 1.0062 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.5070 ± 0.0000 | 639.3112 ± 0.0000 | 1573.1254 ± 0.0000 | 0.8153 ± 0.0000 | 32800 |
| mp-BRKGA | 0.7965 ± 0.0000 | 290.2606 ± 0.0000 | 374.8534 ± 0.0000 | 0.8836 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.5103 ± 0.0000 | 749.6783 ± 0.0000 | 1585.0104 ± 0.0000 | 0.6593 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.633 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.902** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 75.981. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

