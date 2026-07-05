# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.6411 ± 0.0000 | 1869.4941 ± 0.0000 | 944.6551 ± 0.0000 | 0.8988 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.6332 ± 0.0000 | 845.7604 ± 0.0000 | 940.5168 ± 0.0000 | 0.9055 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.2407 ± 0.0000 | 2476.1634 ± 0.0000 | 2897.3496 ± 0.0000 | 0.9512 ± 0.0000 | 65600 |
| mp-BRKGA | 0.1923 ± 0.0000 | 2909.7220 ± 0.0000 | 2341.2531 ± 0.0000 | 0.8341 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.0619 ± 0.0000 | 3793.6691 ± 0.0000 | 4995.2150 ± 0.0000 | 0.9185 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

