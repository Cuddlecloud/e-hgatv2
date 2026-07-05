# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9504 ± 0.0000 | 21.8083 ± 0.0000 | 26.2281 ± 0.0000 | 0.8528 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7659 ± 0.0000 | 163.5286 ± 0.0000 | 230.3865 ± 0.0000 | 0.8442 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.4256 ± 0.0000 | 412.0938 ± 0.0000 | 750.3191 ± 0.0000 | 0.8430 ± 0.0000 | 16400 |
| mp-BRKGA | 0.7101 ± 0.0000 | 294.6350 ± 0.0000 | 168.6401 ± 0.0000 | 0.9506 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.4798 ± 0.0000 | 415.1293 ± 0.0000 | 464.7187 ± 0.0000 | 0.9576 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

