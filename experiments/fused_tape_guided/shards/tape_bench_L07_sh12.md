# Faithful-guidance study -- L07 (N=8, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 40x4 = GAT/BRKGA 160/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9730 ± 0.0412 | 2.2287 ± 3.9039 | 20.1531 ± 33.1361 | 0.8239 ± 0.1444 | 6560 |
| E-HGATv2-attn | 0.9723 ± 0.0311 | 4.7485 ± 7.0422 | 14.8715 ± 27.5786 | 0.8617 ± 0.0904 | 6560 |
| NSGA-II (random) | 0.9364 ± 0.0162 | 6.6503 ± 10.2127 | 38.6641 ± 22.6447 | 0.8714 ± 0.0511 | 6560 |
| mp-BRKGA | 0.9292 ± 0.0282 | 25.1613 ± 15.5643 | 38.1646 ± 29.5943 | 0.8244 ± 0.1333 | 6560 |
| single-pop BRKGA | 0.9290 ± 0.0520 | 9.4714 ± 12.4186 | 41.1211 ± 39.5996 | 0.9069 ± 0.2726 | 6560 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.867 | 0.176 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.985** |
| random baseline | 0.125 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 2.221. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

