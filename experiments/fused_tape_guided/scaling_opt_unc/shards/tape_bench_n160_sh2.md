# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.5622 ± 0.0000 | 2016.1817 ± 0.0000 | 1705.5291 ± 0.0000 | 1.0229 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.7194 ± 0.0000 | 780.9780 ± 0.0000 | 829.9846 ± 0.0000 | 0.8842 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0772 ± 0.0000 | 4326.6437 ± 0.0000 | 4918.0990 ± 0.0000 | 0.8471 ± 0.0000 | 131200 |
| mp-BRKGA | 0.1399 ± 0.0000 | 6099.2602 ± 0.0000 | 3788.7901 ± 0.0000 | 0.8456 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0042 ± 0.0000 | 5902.3272 ± 0.0000 | 6002.1722 ± 0.0000 | 0.9714 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

