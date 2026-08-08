# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7191 ± 0.0000 | 62.5600 ± 0.0000 | 2835.3220 ± 0.0000 | 0.8465 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7217 ± 0.0000 | 777.9254 ± 0.0000 | 1640.3070 ± 0.0000 | 0.8202 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.4987 ± 0.0000 | 1223.2933 ± 0.0000 | 3142.9582 ± 0.0000 | 0.9020 ± 0.0000 | 16400 |
| mp-BRKGA | 0.8104 ± 0.0000 | 303.3971 ± 0.0000 | 490.9814 ± 0.0000 | 0.9601 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.5036 ± 0.0000 | 1187.6008 ± 0.0000 | 2103.3034 ± 0.0000 | 0.9044 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

