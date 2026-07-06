# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7664 ± 0.0000 | 554.8144 ± 0.0000 | 897.6337 ± 0.0000 | 0.8401 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.7878 ± 0.0000 | 400.3537 ± 0.0000 | 406.3837 ± 0.0000 | 0.7448 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.1736 ± 0.0000 | 2647.9931 ± 0.0000 | 4666.5544 ± 0.0000 | 0.9246 ± 0.0000 | 131200 |
| mp-BRKGA | 0.2045 ± 0.0000 | 2206.3216 ± 0.0000 | 1915.3630 ± 0.0000 | 0.7606 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.1104 ± 0.0000 | 2245.6852 ± 0.0000 | 4693.0869 ± 0.0000 | 0.8639 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

