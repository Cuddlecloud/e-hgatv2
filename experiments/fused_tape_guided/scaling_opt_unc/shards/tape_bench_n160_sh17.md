# Faithful-guidance study -- toy:160 (N=160, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.6010 ± 0.0000 | 1920.9551 ± 0.0000 | 853.9494 ± 0.0000 | 0.7332 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.7479 ± 0.0000 | 1176.3677 ± 0.0000 | 478.4272 ± 0.0000 | 0.9370 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0000 ± 0.0000 | 5826.9961 ± 0.0000 | 5160.7802 ± 0.0000 | 0.8756 ± 0.0000 | 131200 |
| mp-BRKGA | 0.0000 ± 0.0000 | 6177.5552 ± 0.0000 | 4308.9862 ± 0.0000 | 0.8483 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0077 ± 0.0000 | 7327.2761 ± 0.0000 | 6530.2263 ± 0.0000 | 0.8398 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.767 | 0.027 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.959** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 62.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

