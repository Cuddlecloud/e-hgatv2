# Faithful-guidance study -- toy:15 (N=15, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 75x4 = GAT/BRKGA 300/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8853 ± 0.0776 | 60.5521 ± 42.7952 | 93.3060 ± 108.6635 | 0.9700 ± 0.1484 | 12300 |
| E-HGATv2-attn | 0.8611 ± 0.1271 | 64.5354 ± 78.4968 | 107.7115 ± 144.0732 | 0.9453 ± 0.1024 | 12300 |
| NSGA-II (random) | 0.7565 ± 0.0410 | 115.0044 ± 20.9336 | 167.8114 ± 74.2101 | 0.8310 ± 0.1628 | 12300 |
| mp-BRKGA | 0.7565 ± 0.0856 | 224.9769 ± 127.8688 | 256.2215 ± 149.8186 | 0.8536 ± 0.1187 | 12300 |
| single-pop BRKGA | 0.7817 ± 0.0413 | 96.5121 ± 27.2207 | 156.4033 ± 129.7180 | 0.8558 ± 0.1023 | 12300 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.800 | 0.081 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.067 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.749. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

