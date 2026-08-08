# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8316 ± 0.0000 | 81.2743 ± 0.0000 | 701.2815 ± 0.0000 | 0.9090 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.8805 ± 0.0000 | 17.5929 ± 0.0000 | 450.4787 ± 0.0000 | 0.8935 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.6579 ± 0.0000 | 434.0747 ± 0.0000 | 1297.9810 ± 0.0000 | 0.9973 ± 0.0000 | 32800 |
| mp-BRKGA | 0.9347 ± 0.0000 | 100.4748 ± 0.0000 | 123.0325 ± 0.0000 | 0.7268 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.5824 ± 0.0000 | 435.5951 ± 0.0000 | 1900.1466 ± 0.0000 | 0.8629 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

