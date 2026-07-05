# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.4310 ± 0.0000 | 1176.0749 ± 0.0000 | 2002.2560 ± 0.0000 | 0.8895 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.5411 ± 0.0000 | 1283.3513 ± 0.0000 | 1170.9144 ± 0.0000 | 0.8756 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.1098 ± 0.0000 | 3766.8260 ± 0.0000 | 4028.0450 ± 0.0000 | 0.9021 ± 0.0000 | 65600 |
| mp-BRKGA | 0.2987 ± 0.0000 | 2712.2227 ± 0.0000 | 1458.4411 ± 0.0000 | 0.8757 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.0489 ± 0.0000 | 4200.3432 ± 0.0000 | 4916.1285 ± 0.0000 | 0.8830 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

