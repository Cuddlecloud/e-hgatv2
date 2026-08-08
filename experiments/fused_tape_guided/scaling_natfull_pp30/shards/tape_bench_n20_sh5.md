# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8682 ± 0.0000 | 153.2280 ± 0.0000 | 183.3320 ± 0.0000 | 1.0629 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.6695 ± 0.0000 | 203.7339 ± 0.0000 | 266.2262 ± 0.0000 | 1.0201 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.5901 ± 0.0000 | 295.9963 ± 0.0000 | 526.7249 ± 0.0000 | 0.8177 ± 0.0000 | 16400 |
| mp-BRKGA | 0.8195 ± 0.0000 | 354.4863 ± 0.0000 | 48.7126 ± 0.0000 | 1.1039 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.7141 ± 0.0000 | 62.6046 ± 0.0000 | 374.2195 ± 0.0000 | 0.9695 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

