# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7721 ± 0.0000 | 105.0437 ± 0.0000 | 922.9296 ± 0.0000 | 0.8283 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.6394 ± 0.0000 | 718.5936 ± 0.0000 | 1115.0500 ± 0.0000 | 0.9090 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.4403 ± 0.0000 | 591.4256 ± 0.0000 | 1928.7462 ± 0.0000 | 0.8484 ± 0.0000 | 65600 |
| mp-BRKGA | 0.8572 ± 0.0000 | 30.7245 ± 0.0000 | 171.8352 ± 0.0000 | 0.9412 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.3110 ± 0.0000 | 819.8784 ± 0.0000 | 2641.8873 ± 0.0000 | 0.8573 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

