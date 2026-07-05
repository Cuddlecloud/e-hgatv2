# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.5856 ± 0.0000 | 1171.3373 ± 0.0000 | 1119.8424 ± 0.0000 | 0.9084 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.7190 ± 0.0000 | 538.4143 ± 0.0000 | 661.9991 ± 0.0000 | 0.8636 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0552 ± 0.0000 | 3543.9921 ± 0.0000 | 4678.6358 ± 0.0000 | 0.9000 ± 0.0000 | 131200 |
| mp-BRKGA | 0.0000 ± 0.0000 | 5745.3612 ± 0.0000 | 4324.8136 ± 0.0000 | 0.7814 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0000 ± 0.0000 | 5336.8562 ± 0.0000 | 6083.4703 ± 0.0000 | 0.8653 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

