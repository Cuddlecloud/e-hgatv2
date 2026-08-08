# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.5795 ± 0.0000 | 493.8076 ± 0.0000 | 749.9336 ± 0.0000 | 0.8989 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7439 ± 0.0000 | 523.1287 ± 0.0000 | 385.8731 ± 0.0000 | 0.8582 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.2866 ± 0.0000 | 1191.8241 ± 0.0000 | 1244.3017 ± 0.0000 | 0.9353 ± 0.0000 | 16400 |
| mp-BRKGA | 0.7074 ± 0.0000 | 2061.1130 ± 0.0000 | 246.9881 ± 0.0000 | 1.0336 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.2083 ± 0.0000 | 1713.5710 ± 0.0000 | 1409.9474 ± 0.0000 | 0.8435 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

