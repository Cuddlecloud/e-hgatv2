# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9104 ± 0.0000 | 215.0690 ± 0.0000 | 200.2260 ± 0.0000 | 0.8717 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.9129 ± 0.0000 | 24.4794 ± 0.0000 | 85.1022 ± 0.0000 | 0.9406 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.4336 ± 0.0000 | 1027.8660 ± 0.0000 | 1106.0780 ± 0.0000 | 0.6926 ± 0.0000 | 65600 |
| mp-BRKGA | 0.5343 ± 0.0000 | 664.6429 ± 0.0000 | 617.0888 ± 0.0000 | 0.8236 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.4455 ± 0.0000 | 669.5462 ± 0.0000 | 866.6376 ± 0.0000 | 0.6495 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

