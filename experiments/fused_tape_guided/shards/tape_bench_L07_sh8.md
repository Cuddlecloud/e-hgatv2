# Faithful-guidance study -- L07 (N=8, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 40x4 = GAT/BRKGA 160/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9623 ± 0.0309 | 5.0259 ± 3.9803 | 24.5574 ± 32.1513 | 0.8363 ± 0.0878 | 6560 |
| E-HGATv2-attn | 0.9656 ± 0.0269 | 3.6175 ± 2.7080 | 15.2055 ± 25.0767 | 0.8424 ± 0.0364 | 6560 |
| NSGA-II (random) | 0.9281 ± 0.0266 | 8.7265 ± 6.1798 | 42.2067 ± 23.1881 | 0.8704 ± 0.0901 | 6560 |
| mp-BRKGA | 0.9298 ± 0.0312 | 25.9925 ± 10.6446 | 34.4722 ± 20.6402 | 0.7681 ± 0.0836 | 6560 |
| single-pop BRKGA | 0.9182 ± 0.0516 | 7.3103 ± 1.6283 | 47.9488 ± 47.2828 | 1.0008 ± 0.1022 | 6560 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.867 | 0.176 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.985** |
| random baseline | 0.125 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 2.221. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

