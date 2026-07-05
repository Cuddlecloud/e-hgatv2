# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7358 ± 0.0000 | 1083.7181 ± 0.0000 | 533.4603 ± 0.0000 | 0.8104 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.5977 ± 0.0000 | 1352.7090 ± 0.0000 | 711.2105 ± 0.0000 | 0.8532 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0026 ± 0.0000 | 4200.6295 ± 0.0000 | 5193.5166 ± 0.0000 | 0.8622 ± 0.0000 | 131200 |
| mp-BRKGA | 0.0000 ± 0.0000 | 6142.3142 ± 0.0000 | 4559.4608 ± 0.0000 | 0.8005 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0000 ± 0.0000 | 6260.0401 ± 0.0000 | 6259.6936 ± 0.0000 | 0.7779 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

