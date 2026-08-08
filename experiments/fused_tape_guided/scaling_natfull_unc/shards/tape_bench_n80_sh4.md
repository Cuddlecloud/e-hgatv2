# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9381 ± 0.0000 | 0.6070 ± 0.0000 | 260.7545 ± 0.0000 | 0.8113 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.7723 ± 0.0000 | 738.3223 ± 0.0000 | 631.5808 ± 0.0000 | 0.8645 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.4346 ± 0.0000 | 1633.0574 ± 0.0000 | 1657.5117 ± 0.0000 | 0.8775 ± 0.0000 | 65600 |
| mp-BRKGA | 0.7176 ± 0.0000 | 1050.5902 ± 0.0000 | 566.0727 ± 0.0000 | 0.8454 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.3438 ± 0.0000 | 2237.8771 ± 0.0000 | 2133.2540 ± 0.0000 | 0.8510 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

