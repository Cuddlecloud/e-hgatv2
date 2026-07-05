# Faithful-guidance study -- toy:20 (N=20, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.6873 ± 0.0000 | 415.4835 ± 0.0000 | 186.6884 ± 0.0000 | 1.0788 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.5619 ± 0.0000 | 350.2934 ± 0.0000 | 236.5716 ± 0.0000 | 0.9725 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.1891 ± 0.0000 | 395.3155 ± 0.0000 | 628.0025 ± 0.0000 | 0.9800 ± 0.0000 | 16400 |
| mp-BRKGA | 0.7407 ± 0.0000 | 688.3832 ± 0.0000 | 146.1234 ± 0.0000 | 1.0082 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.2798 ± 0.0000 | 645.8966 ± 0.0000 | 483.8258 ± 0.0000 | 0.8757 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

