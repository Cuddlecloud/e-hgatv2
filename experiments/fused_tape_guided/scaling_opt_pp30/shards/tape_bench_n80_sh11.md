# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.6633 ± 0.0000 | 160.8041 ± 0.0000 | 1549.6013 ± 0.0000 | 0.9073 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.7686 ± 0.0000 | 499.8669 ± 0.0000 | 681.3634 ± 0.0000 | 0.7892 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.3271 ± 0.0000 | 1126.0371 ± 0.0000 | 3536.3097 ± 0.0000 | 0.7800 ± 0.0000 | 65600 |
| mp-BRKGA | 0.7702 ± 0.0000 | 352.8507 ± 0.0000 | 427.5472 ± 0.0000 | 0.8001 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.2061 ± 0.0000 | 1505.1832 ± 0.0000 | 4192.4783 ± 0.0000 | 0.8850 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

