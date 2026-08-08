# Faithful-guidance study -- L21 (N=12, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 60x4 = GAT/BRKGA 240/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8992 ± 0.0169 | 9.8042 ± 12.7974 | 11.2632 ± 8.5968 | 0.7958 ± 0.0626 | 9840 |
| E-HGATv2-attn | 0.9199 ± 0.1059 | 5.1069 ± 9.9616 | 7.6287 ± 8.6441 | 0.8060 ± 0.1931 | 9840 |
| NSGA-II (random) | 0.8253 ± 0.0499 | 22.0822 ± 17.0772 | 19.6966 ± 7.5875 | 0.9030 ± 0.0885 | 9840 |
| mp-BRKGA | 0.7837 ± 0.0877 | 72.6487 ± 63.8895 | 28.5935 ± 9.8272 | 0.9085 ± 0.2919 | 9840 |
| single-pop BRKGA | 0.8828 ± 0.0803 | 10.5909 ± 9.1293 | 18.5573 ± 8.8244 | 0.7426 ± 0.0661 | 9840 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.054 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.988** |
| random baseline | 0.083 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 2.184. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

