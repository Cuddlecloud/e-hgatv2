# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7769 ± 0.0000 | 76.1770 ± 0.0000 | 882.8736 ± 0.0000 | 0.8661 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.8110 ± 0.0000 | 190.5058 ± 0.0000 | 660.1028 ± 0.0000 | 0.9230 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.6970 ± 0.0000 | 397.4252 ± 0.0000 | 850.9139 ± 0.0000 | 0.8578 ± 0.0000 | 32800 |
| mp-BRKGA | 0.9027 ± 0.0000 | 53.4722 ± 0.0000 | 151.2653 ± 0.0000 | 1.0690 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.5611 ± 0.0000 | 467.5681 ± 0.0000 | 1327.7798 ± 0.0000 | 0.6999 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

