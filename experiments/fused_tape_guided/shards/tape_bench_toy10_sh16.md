# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 1.0298 ± 0.0612 | 2.9139 ± 3.8047 | 20.2224 ± 47.7162 | 0.9775 ± 0.1521 | 8200 |
| E-HGATv2-attn | 1.0430 ± 0.0789 | 2.7349 ± 6.8275 | 5.1740 ± 6.0428 | 0.9198 ± 0.1478 | 8200 |
| NSGA-II (random) | 0.9677 ± 0.0653 | 12.8483 ± 23.9149 | 42.2295 ± 43.6246 | 0.8783 ± 0.0676 | 8200 |
| mp-BRKGA | 0.9434 ± 0.0906 | 32.4983 ± 48.5658 | 33.2944 ± 42.8245 | 0.8479 ± 0.1317 | 8200 |
| single-pop BRKGA | 0.9799 ± 0.0420 | 5.7523 ± 16.7251 | 44.9678 ± 61.7511 | 0.9861 ± 0.1122 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

