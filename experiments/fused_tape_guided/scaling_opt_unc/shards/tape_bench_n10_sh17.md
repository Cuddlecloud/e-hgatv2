# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9750 ± 0.0000 | 7.2287 ± 0.0000 | 8.6948 ± 0.0000 | 0.9578 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.8466 ± 0.0000 | 47.9311 ± 0.0000 | 62.0363 ± 0.0000 | 0.9385 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.8939 ± 0.0000 | 43.7971 ± 0.0000 | 44.5482 ± 0.0000 | 0.8191 ± 0.0000 | 8200 |
| mp-BRKGA | 0.6658 ± 0.0000 | 480.1629 ± 0.0000 | 156.4843 ± 0.0000 | 0.8557 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.7340 ± 0.0000 | 99.4724 ± 0.0000 | 178.5612 ± 0.0000 | 0.7303 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

