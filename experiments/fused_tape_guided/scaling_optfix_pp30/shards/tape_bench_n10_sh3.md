# Faithful-guidance study -- toy:10 (N=10, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9404 ± 0.0000 | 21.9517 ± 0.0000 | 17.4027 ± 0.0000 | 0.8687 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.9408 ± 0.0000 | 1.9692 ± 0.0000 | 26.7384 ± 0.0000 | 0.9590 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.9261 ± 0.0000 | 11.5071 ± 0.0000 | 31.1796 ± 0.0000 | 0.8470 ± 0.0000 | 16400 |
| mp-BRKGA | 0.7682 ± 0.0000 | 59.5278 ± 0.0000 | 111.2904 ± 0.0000 | 1.0415 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.8928 ± 0.0000 | 49.8586 ± 0.0000 | 37.3994 ± 0.0000 | 1.0593 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.080 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.955** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 33.593. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

