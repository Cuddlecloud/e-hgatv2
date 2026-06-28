# Faithful-guidance study -- toy:5 (N=5, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 25x4 = GAT/BRKGA 100/gen). Reference: exact Oracle. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9638 ± 0.0313 | 1.3283 ± 0.2444 | 22.8743 ± 32.9739 | 0.9984 ± 0.0223 | 4100 |
| E-HGATv2-attn | 0.9635 ± 0.0368 | 1.3379 ± 0.8069 | 22.7539 ± 34.6389 | 0.9612 ± 0.0161 | 4100 |
| NSGA-II (random) | 0.9572 ± 0.0352 | 1.8570 ± 2.4514 | 24.4687 ± 33.2834 | 0.9490 ± 0.0383 | 4100 |
| mp-BRKGA | 0.9185 ± 0.0363 | 36.9832 ± 32.8030 | 39.9197 ± 20.7611 | 0.8587 ± 0.0711 | 4100 |
| single-pop BRKGA | 0.9491 ± 0.0331 | 1.8129 ± 1.4330 | 33.7399 ± 31.0390 | 0.9299 ± 0.0318 | 4100 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.062 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.980** |
| random baseline | 0.200 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 8.114. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

