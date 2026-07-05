# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9818 ± 0.0000 | 7.8082 ± 0.0000 | 9.4439 ± 0.0000 | 0.8681 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9543 ± 0.0000 | 20.2073 ± 0.0000 | 22.0850 ± 0.0000 | 0.8542 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.9289 ± 0.0000 | 32.9131 ± 0.0000 | 37.3984 ± 0.0000 | 0.8189 ± 0.0000 | 8200 |
| mp-BRKGA | 0.7925 ± 0.0000 | 329.8802 ± 0.0000 | 110.7677 ± 0.0000 | 0.7561 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.7489 ± 0.0000 | 110.2350 ± 0.0000 | 216.9508 ± 0.0000 | 1.0034 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

