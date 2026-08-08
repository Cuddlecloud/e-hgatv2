# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9569 ± 0.0000 | 16.4585 ± 0.0000 | 41.5536 ± 0.0000 | 0.9092 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.9710 ± 0.0000 | 5.3167 ± 0.0000 | 31.8372 ± 0.0000 | 0.8686 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.9531 ± 0.0000 | 11.4586 ± 0.0000 | 47.0396 ± 0.0000 | 0.8742 ± 0.0000 | 16400 |
| mp-BRKGA | 0.9046 ± 0.0000 | 56.6503 ± 0.0000 | 63.3980 ± 0.0000 | 0.8384 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.9269 ± 0.0000 | 15.8736 ± 0.0000 | 51.0534 ± 0.0000 | 1.0529 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

