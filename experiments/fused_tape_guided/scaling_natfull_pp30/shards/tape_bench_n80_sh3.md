# Faithful-guidance study -- toy:80 (N=80, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8645 ± 0.0000 | 110.3581 ± 0.0000 | 187.9069 ± 0.0000 | 0.7188 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.7535 ± 0.0000 | 168.6127 ± 0.0000 | 434.0721 ± 0.0000 | 0.7623 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.3413 ± 0.0000 | 1049.2083 ± 0.0000 | 1747.6002 ± 0.0000 | 0.9446 ± 0.0000 | 65600 |
| mp-BRKGA | 0.7337 ± 0.0000 | 1815.6279 ± 0.0000 | 333.1469 ± 0.0000 | 0.5981 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.1791 ± 0.0000 | 1946.7205 ± 0.0000 | 2276.2615 ± 0.0000 | 0.7804 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.005 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.925** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 127.976. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

