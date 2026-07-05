# Faithful-guidance study -- toy:40 (N=40, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8138 ± 0.0000 | 161.2172 ± 0.0000 | 295.4682 ± 0.0000 | 1.0539 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.8717 ± 0.0000 | 34.3999 ± 0.0000 | 67.8533 ± 0.0000 | 1.0056 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.3407 ± 0.0000 | 572.9945 ± 0.0000 | 1479.9694 ± 0.0000 | 0.9166 ± 0.0000 | 32800 |
| mp-BRKGA | 0.6612 ± 0.0000 | 375.9459 ± 0.0000 | 292.0195 ± 0.0000 | 0.8998 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.3201 ± 0.0000 | 628.4071 ± 0.0000 | 1285.7644 ± 0.0000 | 0.6567 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.633 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.902** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 75.981. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

