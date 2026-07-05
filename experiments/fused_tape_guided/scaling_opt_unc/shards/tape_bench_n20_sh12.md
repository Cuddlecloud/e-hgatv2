# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7936 ± 0.0000 | 82.3358 ± 0.0000 | 219.8002 ± 0.0000 | 0.9348 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7668 ± 0.0000 | 151.1556 ± 0.0000 | 160.9693 ± 0.0000 | 1.0168 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.5430 ± 0.0000 | 364.8417 ± 0.0000 | 454.1018 ± 0.0000 | 0.9330 ± 0.0000 | 16400 |
| mp-BRKGA | 0.5891 ± 0.0000 | 684.1186 ± 0.0000 | 310.1337 ± 0.0000 | 0.9599 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.6993 ± 0.0000 | 226.9646 ± 0.0000 | 269.0305 ± 0.0000 | 0.7606 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

