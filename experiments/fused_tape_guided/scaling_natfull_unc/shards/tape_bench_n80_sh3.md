# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7901 ± 0.0000 | 326.2402 ± 0.0000 | 821.6060 ± 0.0000 | 0.8013 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.9475 ± 0.0000 | 38.1716 ± 0.0000 | 209.3138 ± 0.0000 | 0.8010 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.4792 ± 0.0000 | 987.5223 ± 0.0000 | 1772.7319 ± 0.0000 | 0.9718 ± 0.0000 | 65600 |
| mp-BRKGA | 0.7832 ± 0.0000 | 272.7026 ± 0.0000 | 389.3389 ± 0.0000 | 0.8788 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.4245 ± 0.0000 | 1226.3016 ± 0.0000 | 2181.5773 ± 0.0000 | 0.8770 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

