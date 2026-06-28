# Faithful-guidance study -- L35 (N=12, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 60x4 = GAT/BRKGA 240/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9690 ± 0.0294 | 13.8948 ± 10.1637 | 15.2829 ± 11.0804 | 0.8718 ± 0.0543 | 9840 |
| E-HGATv2-attn | 0.9765 ± 0.0424 | 10.7492 ± 12.7562 | 12.2218 ± 12.2688 | 0.9280 ± 0.1397 | 9840 |
| NSGA-II (random) | 0.9337 ± 0.0245 | 30.4441 ± 16.8280 | 32.6962 ± 13.4698 | 0.8714 ± 0.1474 | 9840 |
| mp-BRKGA | 0.9364 ± 0.0535 | 36.8125 ± 17.8370 | 43.5216 ± 16.6157 | 0.8455 ± 0.1599 | 9840 |
| single-pop BRKGA | 0.9300 ± 0.0154 | 16.3297 ± 9.3955 | 27.1993 ± 12.6069 | 0.9523 ± 0.0587 | 9840 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.084 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.989** |
| random baseline | 0.083 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 7.821. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

