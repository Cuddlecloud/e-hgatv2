# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.5046 ± 0.0000 | 1592.3978 ± 0.0000 | 1419.5714 ± 0.0000 | 0.8406 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.5252 ± 0.0000 | 2228.3437 ± 0.0000 | 1232.4071 ± 0.0000 | 0.7954 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.1427 ± 0.0000 | 4405.8682 ± 0.0000 | 3882.3295 ± 0.0000 | 0.9732 ± 0.0000 | 65600 |
| mp-BRKGA | 0.2572 ± 0.0000 | 2858.3145 ± 0.0000 | 1785.9141 ± 0.0000 | 0.6863 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.0562 ± 0.0000 | 3366.2231 ± 0.0000 | 4562.5063 ± 0.0000 | 0.8245 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

