# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7902 ± 0.0000 | 180.9389 ± 0.0000 | 615.1240 ± 0.0000 | 0.9257 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.7987 ± 0.0000 | 218.1359 ± 0.0000 | 493.8322 ± 0.0000 | 0.9480 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.5282 ± 0.0000 | 667.4433 ± 0.0000 | 1438.4218 ± 0.0000 | 0.9972 ± 0.0000 | 32800 |
| mp-BRKGA | 0.8397 ± 0.0000 | 504.6320 ± 0.0000 | 370.9710 ± 0.0000 | 0.7755 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.4303 ± 0.0000 | 618.0252 ± 0.0000 | 2177.8299 ± 0.0000 | 0.8386 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

