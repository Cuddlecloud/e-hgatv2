# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9729 ± 0.0000 | 82.9280 ± 0.0000 | 114.8209 ± 0.0000 | 0.7487 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.6634 ± 0.0000 | 489.3896 ± 0.0000 | 466.8964 ± 0.0000 | 0.8720 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.0825 ± 0.0000 | 2450.8080 ± 0.0000 | 5816.1243 ± 0.0000 | 0.8211 ± 0.0000 | 131200 |
| mp-BRKGA | 0.1049 ± 0.0000 | 2569.9071 ± 0.0000 | 4135.5012 ± 0.0000 | 0.9458 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.0725 ± 0.0000 | 2553.6929 ± 0.0000 | 5485.1648 ± 0.0000 | 0.7596 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

