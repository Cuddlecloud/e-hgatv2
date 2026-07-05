# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9004 ± 0.0000 | 163.3360 ± 0.0000 | 318.3831 ± 0.0000 | 0.9704 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.9068 ± 0.0000 | 155.8144 ± 0.0000 | 327.0816 ± 0.0000 | 0.8948 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.6755 ± 0.0000 | 492.2254 ± 0.0000 | 1480.3832 ± 0.0000 | 1.0245 ± 0.0000 | 32800 |
| mp-BRKGA | 0.8403 ± 0.0000 | 235.2134 ± 0.0000 | 524.3434 ± 0.0000 | 0.7961 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.5935 ± 0.0000 | 575.8519 ± 0.0000 | 2013.2133 ± 0.0000 | 0.8634 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

