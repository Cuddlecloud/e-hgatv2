# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8539 ± 0.0000 | 93.6119 ± 0.0000 | 355.2468 ± 0.0000 | 0.8868 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.8684 ± 0.0000 | 152.8172 ± 0.0000 | 231.8197 ± 0.0000 | 0.9089 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.5586 ± 0.0000 | 663.1514 ± 0.0000 | 1390.3187 ± 0.0000 | 0.8677 ± 0.0000 | 32800 |
| mp-BRKGA | 0.8259 ± 0.0000 | 198.7789 ± 0.0000 | 420.5322 ± 0.0000 | 0.7984 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.5087 ± 0.0000 | 653.1527 ± 0.0000 | 1573.1764 ± 0.0000 | 0.9206 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

