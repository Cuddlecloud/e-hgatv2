# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9414 ± 0.0000 | 36.5473 ± 0.0000 | 26.9401 ± 0.0000 | 1.1381 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.9259 ± 0.0000 | 25.9523 ± 0.0000 | 32.3283 ± 0.0000 | 0.8731 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.8457 ± 0.0000 | 50.1274 ± 0.0000 | 44.0808 ± 0.0000 | 0.9303 ± 0.0000 | 16400 |
| mp-BRKGA | 0.8465 ± 0.0000 | 181.6924 ± 0.0000 | 56.9241 ± 0.0000 | 0.9237 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.9747 ± 0.0000 | 5.4423 ± 0.0000 | 7.8591 ± 0.0000 | 0.8317 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

