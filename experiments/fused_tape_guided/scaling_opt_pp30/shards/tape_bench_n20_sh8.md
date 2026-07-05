# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.5987 ± 0.0000 | 115.9060 ± 0.0000 | 156.0895 ± 0.0000 | 1.0212 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.5980 ± 0.0000 | 161.6653 ± 0.0000 | 158.6763 ± 0.0000 | 1.0387 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.2134 ± 0.0000 | 493.6261 ± 0.0000 | 415.1745 ± 0.0000 | 0.8511 ± 0.0000 | 16400 |
| mp-BRKGA | 0.7338 ± 0.0000 | 448.5361 ± 0.0000 | 55.6385 ± 0.0000 | 1.2523 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.3980 ± 0.0000 | 200.2992 ± 0.0000 | 299.5898 ± 0.0000 | 0.7669 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

