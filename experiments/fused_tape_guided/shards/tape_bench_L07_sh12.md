# Faithful-guidance study -- L07 (N=8, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 40x4 = GAT/BRKGA 160/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9568 ± 0.0522 | 11.4877 ± 24.0048 | 25.3254 ± 36.3705 | 0.8240 ± 0.1875 | 6560 |
| E-HGATv2-attn | 0.9551 ± 0.0273 | 6.6016 ± 8.3402 | 20.5572 ± 22.6245 | 0.8059 ± 0.0794 | 6560 |
| NSGA-II (random) | 0.9129 ± 0.0069 | 17.0314 ± 14.2833 | 48.0072 ± 13.4631 | 0.9090 ± 0.0611 | 6560 |
| mp-BRKGA | 0.9032 ± 0.0225 | 35.1876 ± 22.3491 | 47.0212 ± 22.1463 | 0.7818 ± 0.0895 | 6560 |
| single-pop BRKGA | 0.9208 ± 0.0532 | 9.8632 ± 11.7575 | 41.2064 ± 36.0400 | 0.8390 ± 0.0667 | 6560 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.867 | 0.176 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.985** |
| random baseline | 0.125 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 2.221. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

