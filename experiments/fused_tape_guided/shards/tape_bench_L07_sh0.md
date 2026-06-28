# Faithful-guidance study -- L07 (N=8, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 40x4 = GAT/BRKGA 160/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9621 ± 0.0333 | 3.4985 ± 3.1054 | 31.1440 ± 28.6330 | 0.7806 ± 0.1204 | 6560 |
| E-HGATv2-attn | 0.9848 ± 0.0086 | 1.5479 ± 2.0813 | 7.6574 ± 8.8827 | 0.8348 ± 0.1228 | 6560 |
| NSGA-II (random) | 0.9566 ± 0.0320 | 8.6922 ± 13.3956 | 26.2014 ± 28.0642 | 0.8738 ± 0.2394 | 6560 |
| mp-BRKGA | 0.9116 ± 0.0687 | 39.8753 ± 48.3578 | 38.5432 ± 29.7613 | 0.7840 ± 0.1612 | 6560 |
| single-pop BRKGA | 0.9341 ± 0.0287 | 8.5405 ± 11.3184 | 35.4945 ± 31.8312 | 0.8562 ± 0.1059 | 6560 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.867 | 0.176 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.985** |
| random baseline | 0.125 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 2.221. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

