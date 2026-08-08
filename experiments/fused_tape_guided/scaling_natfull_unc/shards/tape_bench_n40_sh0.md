# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8399 ± 0.0000 | 82.7807 ± 0.0000 | 483.8112 ± 0.0000 | 0.9882 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.7449 ± 0.0000 | 207.2568 ± 0.0000 | 850.0635 ± 0.0000 | 0.8978 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.6138 ± 0.0000 | 359.7510 ± 0.0000 | 1424.3494 ± 0.0000 | 0.9240 ± 0.0000 | 32800 |
| mp-BRKGA | 0.9780 ± 0.0000 | 0.0000 ± 0.0000 | 33.2804 ± 0.0000 | 0.9467 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.6163 ± 0.0000 | 402.7362 ± 0.0000 | 1248.4855 ± 0.0000 | 0.9157 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

