# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9037 ± 0.0000 | 36.5951 ± 0.0000 | 37.7079 ± 0.0000 | 1.1329 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9689 ± 0.0000 | 8.9821 ± 0.0000 | 10.5323 ± 0.0000 | 0.8837 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.6968 ± 0.0000 | 91.0361 ± 0.0000 | 160.0775 ± 0.0000 | 0.7913 ± 0.0000 | 8200 |
| mp-BRKGA | 0.8298 ± 0.0000 | 47.3930 ± 0.0000 | 85.6432 ± 0.0000 | 0.9161 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.9151 ± 0.0000 | 14.6888 ± 0.0000 | 33.7010 ± 0.0000 | 0.9476 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

