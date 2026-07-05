# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.5044 ± 0.0000 | 2615.3727 ± 0.0000 | 2202.0717 ± 0.0000 | 0.8711 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.8327 ± 0.0000 | 574.0960 ± 0.0000 | 475.4004 ± 0.0000 | 0.7916 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0668 ± 0.0000 | 5650.1145 ± 0.0000 | 6237.4326 ± 0.0000 | 0.9194 ± 0.0000 | 131200 |
| mp-BRKGA | 0.4936 ± 0.0000 | 3952.5832 ± 0.0000 | 2116.8900 ± 0.0000 | 0.7363 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0576 ± 0.0000 | 6123.9901 ± 0.0000 | 6660.1463 ± 0.0000 | 0.9024 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

