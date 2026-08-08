# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7757 ± 0.0000 | 600.2121 ± 0.0000 | 1025.5608 ± 0.0000 | 0.9055 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.8270 ± 0.0000 | 138.9039 ± 0.0000 | 941.3096 ± 0.0000 | 0.9070 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.6021 ± 0.0000 | 858.5883 ± 0.0000 | 1926.4038 ± 0.0000 | 0.8978 ± 0.0000 | 16400 |
| mp-BRKGA | 0.8825 ± 0.0000 | 257.0632 ± 0.0000 | 490.9646 ± 0.0000 | 1.0688 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.6349 ± 0.0000 | 543.7747 ± 0.0000 | 1947.9288 ± 0.0000 | 0.8551 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

