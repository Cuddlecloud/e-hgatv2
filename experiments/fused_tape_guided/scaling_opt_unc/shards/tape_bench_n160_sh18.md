# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.5711 ± 0.0000 | 1145.7969 ± 0.0000 | 1411.1270 ± 0.0000 | 0.9394 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.4570 ± 0.0000 | 1837.8736 ± 0.0000 | 1094.5085 ± 0.0000 | 0.7355 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0000 ± 0.0000 | 5580.3631 ± 0.0000 | 5939.5110 ± 0.0000 | 0.9858 ± 0.0000 | 131200 |
| mp-BRKGA | 0.0493 ± 0.0000 | 5439.1627 ± 0.0000 | 2102.4973 ± 0.0000 | 0.6935 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0000 ± 0.0000 | 5682.9423 ± 0.0000 | 5719.1427 ± 0.0000 | 0.8574 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

