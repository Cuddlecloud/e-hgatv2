# Faithful-guidance study -- toy:40 (N=40, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8752 ± 0.0000 | 66.2941 ± 0.0000 | 110.0220 ± 0.0000 | 0.9529 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.9718 ± 0.0000 | 25.8139 ± 0.0000 | 51.8456 ± 0.0000 | 0.8121 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.4485 ± 0.0000 | 395.6531 ± 0.0000 | 1214.4460 ± 0.0000 | 0.9382 ± 0.0000 | 32800 |
| mp-BRKGA | 0.7858 ± 0.0000 | 167.6168 ± 0.0000 | 220.1214 ± 0.0000 | 1.0656 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.4017 ± 0.0000 | 644.7876 ± 0.0000 | 1338.9875 ± 0.0000 | 0.7666 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.633 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.902** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 75.981. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

