# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9653 ± 0.0000 | 13.4376 ± 0.0000 | 15.5802 ± 0.0000 | 0.8740 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.9646 ± 0.0000 | 21.7037 ± 0.0000 | 35.4543 ± 0.0000 | 1.0314 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.9647 ± 0.0000 | 7.3958 ± 0.0000 | 56.0806 ± 0.0000 | 0.9447 ± 0.0000 | 16400 |
| mp-BRKGA | 0.9145 ± 0.0000 | 45.6844 ± 0.0000 | 66.3320 ± 0.0000 | 1.0363 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.8831 ± 0.0000 | 58.0415 ± 0.0000 | 141.9058 ± 0.0000 | 0.8582 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

