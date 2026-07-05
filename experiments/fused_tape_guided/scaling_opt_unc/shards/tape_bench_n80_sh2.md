# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7498 ± 0.0000 | 456.9252 ± 0.0000 | 983.6886 ± 0.0000 | 0.8593 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.7059 ± 0.0000 | 688.2516 ± 0.0000 | 747.4253 ± 0.0000 | 0.8560 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.2123 ± 0.0000 | 1861.3495 ± 0.0000 | 4461.8534 ± 0.0000 | 0.8915 ± 0.0000 | 65600 |
| mp-BRKGA | 0.3718 ± 0.0000 | 2132.5042 ± 0.0000 | 1505.8642 ± 0.0000 | 0.9477 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.1740 ± 0.0000 | 2226.4607 ± 0.0000 | 4848.8138 ± 0.0000 | 0.8773 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

