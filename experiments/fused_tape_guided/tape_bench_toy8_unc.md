# Faithful-guidance study -- toy:8 (N=8, uncoupled)

_2 seeds, 12 gens, matched exact-eval budget (mp 32x4 = GAT/BRKGA 128/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 30 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9151 ± 0.2982 | 30.0831 ± 25.1085 | 49.0156 ± 22.4969 | 0.9091 ± 0.8943 | 1664 |
| E-HGATv2-attn | 0.9411 ± 0.0853 | 20.9605 ± 35.7691 | 37.4833 ± 81.0531 | 0.6750 ± 1.4542 | 1664 |
| NSGA-II (random) | 0.8830 ± 0.2843 | 40.0897 ± 43.2743 | 67.9286 ± 25.4845 | 0.8757 ± 0.8029 | 1664 |
| mp-BRKGA | 0.8237 ± 0.1366 | 75.9821 ± 209.6650 | 125.1687 ± 116.5225 | 0.7710 ± 0.1625 | 1664 |
| single-pop BRKGA | 0.7657 ± 0.3183 | 51.7072 ± 45.7034 | 171.4687 ± 463.3539 | 0.8855 ± 0.1667 | 1664 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.800 | 0.058 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.125 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.905. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

