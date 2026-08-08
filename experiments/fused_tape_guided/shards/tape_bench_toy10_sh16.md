# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8322 ± 0.1512 | 69.3811 ± 75.4505 | 94.6045 ± 99.9787 | 0.9713 ± 0.1105 | 8200 |
| E-HGATv2-attn | 0.9011 ± 0.0647 | 32.4217 ± 47.4731 | 48.9336 ± 44.9190 | 0.9296 ± 0.0552 | 8200 |
| NSGA-II (random) | 0.8418 ± 0.0907 | 148.1047 ± 213.1104 | 72.1577 ± 52.5271 | 0.9095 ± 0.0928 | 8200 |
| mp-BRKGA | 0.7990 ± 0.1581 | 231.7384 ± 370.8123 | 92.1053 ± 88.1654 | 0.8296 ± 0.0709 | 8200 |
| single-pop BRKGA | 0.7767 ± 0.1047 | 79.2291 ± 45.3025 | 125.2498 ± 89.2882 | 0.9072 ± 0.2059 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

