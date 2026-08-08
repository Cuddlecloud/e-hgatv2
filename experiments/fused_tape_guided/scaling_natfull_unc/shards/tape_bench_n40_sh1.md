# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9238 ± 0.0000 | 33.2927 ± 0.0000 | 83.0582 ± 0.0000 | 0.9180 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.8604 ± 0.0000 | 41.6635 ± 0.0000 | 148.8786 ± 0.0000 | 0.9014 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.7456 ± 0.0000 | 232.6445 ± 0.0000 | 393.3367 ± 0.0000 | 1.0255 ± 0.0000 | 32800 |
| mp-BRKGA | 0.8505 ± 0.0000 | 93.4374 ± 0.0000 | 174.9872 ± 0.0000 | 0.7792 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.6173 ± 0.0000 | 333.9705 ± 0.0000 | 680.6515 ± 0.0000 | 0.8582 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

