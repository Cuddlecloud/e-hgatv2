# Faithful-guidance study -- L35 (N=12, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 60x4 = GAT/BRKGA 240/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9232 ± 0.0316 | 11.1530 ± 11.0663 | 13.5942 ± 5.1249 | 0.8556 ± 0.1373 | 9840 |
| E-HGATv2-attn | 0.8939 ± 0.0460 | 13.2151 ± 5.5087 | 16.7846 ± 7.6230 | 0.8862 ± 0.1776 | 9840 |
| NSGA-II (random) | 0.8425 ± 0.0480 | 39.6088 ± 17.5448 | 35.3602 ± 17.5964 | 0.8896 ± 0.1738 | 9840 |
| mp-BRKGA | 0.7734 ± 0.0594 | 69.2857 ± 21.4297 | 72.1907 ± 37.4231 | 0.8075 ± 0.1247 | 9840 |
| single-pop BRKGA | 0.8247 ± 0.1136 | 43.8898 ± 42.4171 | 53.9327 ± 24.5632 | 0.8469 ± 0.1091 | 9840 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.084 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.989** |
| random baseline | 0.083 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 7.821. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

