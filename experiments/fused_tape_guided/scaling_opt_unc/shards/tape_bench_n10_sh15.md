# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9598 ± 0.0000 | 19.8091 ± 0.0000 | 20.7116 ± 0.0000 | 0.9126 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.8796 ± 0.0000 | 96.0161 ± 0.0000 | 72.8701 ± 0.0000 | 1.1766 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.9490 ± 0.0000 | 24.5882 ± 0.0000 | 22.1682 ± 0.0000 | 0.8369 ± 0.0000 | 8200 |
| mp-BRKGA | 0.7007 ± 0.0000 | 143.3647 ± 0.0000 | 164.3716 ± 0.0000 | 0.8786 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8586 ± 0.0000 | 33.8867 ± 0.0000 | 70.6489 ± 0.0000 | 1.0725 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

