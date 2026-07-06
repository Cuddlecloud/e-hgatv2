# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9003 ± 0.0000 | 316.7652 ± 0.0000 | 483.9048 ± 0.0000 | 0.9402 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.8611 ± 0.0000 | 463.9474 ± 0.0000 | 492.1128 ± 0.0000 | 0.7480 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.3010 ± 0.0000 | 2442.6745 ± 0.0000 | 4939.0597 ± 0.0000 | 0.8430 ± 0.0000 | 131200 |
| mp-BRKGA | 0.3756 ± 0.0000 | 2523.5806 ± 0.0000 | 3413.7672 ± 0.0000 | 0.6558 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.2912 ± 0.0000 | 2370.7954 ± 0.0000 | 5140.2706 ± 0.0000 | 0.8508 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

