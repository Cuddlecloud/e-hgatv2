# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9297 ± 0.0000 | 93.5131 ± 0.0000 | 163.0232 ± 0.0000 | 1.2331 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.8901 ± 0.0000 | 206.3521 ± 0.0000 | 311.9415 ± 0.0000 | 0.9108 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.6598 ± 0.0000 | 463.2659 ± 0.0000 | 1474.9301 ± 0.0000 | 0.8616 ± 0.0000 | 32800 |
| mp-BRKGA | 0.8349 ± 0.0000 | 254.7450 ± 0.0000 | 445.1165 ± 0.0000 | 0.8154 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.5936 ± 0.0000 | 833.2234 ± 0.0000 | 1855.0818 ± 0.0000 | 0.7857 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

