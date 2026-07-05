# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9776 ± 0.0000 | 25.5079 ± 0.0000 | 13.8546 ± 0.0000 | 1.1250 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7986 ± 0.0000 | 89.0027 ± 0.0000 | 82.3860 ± 0.0000 | 1.0160 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.4371 ± 0.0000 | 314.3747 ± 0.0000 | 577.0311 ± 0.0000 | 0.8733 ± 0.0000 | 16400 |
| mp-BRKGA | 0.2965 ± 0.0000 | 968.4763 ± 0.0000 | 461.1983 ± 0.0000 | 1.1390 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.4992 ± 0.0000 | 247.0525 ± 0.0000 | 273.6186 ± 0.0000 | 0.7756 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

