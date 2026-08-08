# Faithful-guidance study -- toy:20 (N=20, coupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7683 ± 0.0962 | 181.4404 ± 235.7422 | 360.0845 ± 153.3280 | 1.0014 ± 0.1175 | 16400 |
| E-HGATv2-attn | 0.6838 ± 0.0943 | 279.8009 ± 240.7635 | 453.2110 ± 147.1885 | 1.0444 ± 0.1279 | 16400 |
| NSGA-II (random) | 0.4371 ± 0.0862 | 596.0985 ± 251.3618 | 894.9544 ± 164.3100 | 0.8765 ± 0.1068 | 16400 |
| mp-BRKGA | 0.7473 ± 0.1869 | 826.8089 ± 209.4572 | 310.2869 ± 259.3406 | 1.0541 ± 0.1030 | 16400 |
| single-pop BRKGA | 0.6091 ± 0.1454 | 310.5378 ± 86.7969 | 569.3217 ± 268.7045 | 0.8656 ± 0.1293 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

