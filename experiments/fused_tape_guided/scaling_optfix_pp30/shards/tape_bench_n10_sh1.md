# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8851 ± 0.0000 | 53.2621 ± 0.0000 | 66.3431 ± 0.0000 | 0.9275 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.9592 ± 0.0000 | 18.0000 ± 0.0000 | 18.8667 ± 0.0000 | 1.0433 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.9056 ± 0.0000 | 21.4449 ± 0.0000 | 59.2317 ± 0.0000 | 1.0099 ± 0.0000 | 16400 |
| mp-BRKGA | 0.8505 ± 0.0000 | 105.6392 ± 0.0000 | 55.0097 ± 0.0000 | 1.1445 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.7847 ± 0.0000 | 156.7699 ± 0.0000 | 100.5712 ± 0.0000 | 1.0369 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

