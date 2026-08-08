# Faithful-guidance study -- L07 (N=8, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 40x4 = GAT/BRKGA 160/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9668 ± 0.0267 | 7.0698 ± 4.0894 | 18.1615 ± 32.7018 | 0.8431 ± 0.0386 | 6560 |
| E-HGATv2-attn | 0.9672 ± 0.0239 | 4.0010 ± 3.0076 | 14.4359 ± 30.1665 | 0.8451 ± 0.0407 | 6560 |
| NSGA-II (random) | 0.9402 ± 0.0256 | 11.9055 ± 6.9342 | 32.0350 ± 24.8976 | 0.9104 ± 0.0427 | 6560 |
| mp-BRKGA | 0.9289 ± 0.0343 | 24.6808 ± 17.6509 | 39.2128 ± 31.3146 | 0.7877 ± 0.2402 | 6560 |
| single-pop BRKGA | 0.9306 ± 0.0329 | 8.7271 ± 5.2036 | 42.3239 ± 36.1047 | 0.9094 ± 0.0757 | 6560 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.867 | 0.176 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.985** |
| random baseline | 0.125 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 2.221. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

