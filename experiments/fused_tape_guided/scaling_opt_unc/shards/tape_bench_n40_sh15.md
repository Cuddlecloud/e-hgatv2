# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9262 ± 0.0000 | 7.9528 ± 0.0000 | 242.0286 ± 0.0000 | 1.1879 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.8905 ± 0.0000 | 118.7505 ± 0.0000 | 303.6697 ± 0.0000 | 0.9525 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.6864 ± 0.0000 | 413.9557 ± 0.0000 | 1196.1060 ± 0.0000 | 0.8364 ± 0.0000 | 32800 |
| mp-BRKGA | 0.8536 ± 0.0000 | 184.8832 ± 0.0000 | 349.4603 ± 0.0000 | 0.8831 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.5944 ± 0.0000 | 423.6316 ± 0.0000 | 1739.7682 ± 0.0000 | 0.8226 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

