# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8910 ± 0.0000 | 73.6441 ± 0.0000 | 433.8774 ± 0.0000 | 0.8911 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.9175 ± 0.0000 | 75.0274 ± 0.0000 | 280.5394 ± 0.0000 | 0.8784 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.6777 ± 0.0000 | 580.6771 ± 0.0000 | 1194.6194 ± 0.0000 | 0.9039 ± 0.0000 | 32800 |
| mp-BRKGA | 0.7859 ± 0.0000 | 355.6455 ± 0.0000 | 616.9704 ± 0.0000 | 0.8678 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.6000 ± 0.0000 | 621.4603 ± 0.0000 | 1636.2094 ± 0.0000 | 0.8205 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

