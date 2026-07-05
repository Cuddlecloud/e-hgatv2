# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.4167 ± 0.0000 | 2127.3775 ± 0.0000 | 2006.1083 ± 0.0000 | 0.9033 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.6968 ± 0.0000 | 585.9587 ± 0.0000 | 560.9558 ± 0.0000 | 0.7982 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0000 ± 0.0000 | 5350.8387 ± 0.0000 | 5685.3705 ± 0.0000 | 0.9523 ± 0.0000 | 131200 |
| mp-BRKGA | 0.0327 ± 0.0000 | 5931.0149 ± 0.0000 | 4001.3011 ± 0.0000 | 0.8417 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0000 ± 0.0000 | 6063.3193 ± 0.0000 | 6615.7804 ± 0.0000 | 0.8642 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

