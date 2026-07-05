# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9389 ± 0.0000 | 17.9750 ± 0.0000 | 29.2019 ± 0.0000 | 0.9661 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9755 ± 0.0000 | 11.9350 ± 0.0000 | 13.2090 ± 0.0000 | 0.8333 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.7285 ± 0.0000 | 136.0090 ± 0.0000 | 178.6381 ± 0.0000 | 0.9393 ± 0.0000 | 8200 |
| mp-BRKGA | 0.7441 ± 0.0000 | 147.5354 ± 0.0000 | 156.0737 ± 0.0000 | 0.7512 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.7224 ± 0.0000 | 127.7679 ± 0.0000 | 184.1971 ± 0.0000 | 0.9001 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

