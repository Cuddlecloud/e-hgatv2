# Faithful-guidance study -- L07 (N=8, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 40x4 = GAT/BRKGA 160/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9282 ± 0.0139 | 5.8782 ± 5.4086 | 44.4977 ± 6.3103 | 0.7987 ± 0.0389 | 6560 |
| E-HGATv2-attn | 0.9639 ± 0.0359 | 7.3364 ± 8.8060 | 16.2294 ± 29.5493 | 0.8387 ± 0.2221 | 6560 |
| NSGA-II (random) | 0.9404 ± 0.0087 | 11.7729 ± 15.2622 | 26.0716 ± 18.2110 | 0.8885 ± 0.1946 | 6560 |
| mp-BRKGA | 0.8778 ± 0.0438 | 59.6687 ± 50.4756 | 54.4814 ± 17.3334 | 0.8223 ± 0.1431 | 6560 |
| single-pop BRKGA | 0.9272 ± 0.0688 | 12.4983 ± 7.7054 | 30.2259 ± 47.8887 | 0.8482 ± 0.0736 | 6560 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.867 | 0.176 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.985** |
| random baseline | 0.125 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 2.221. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

