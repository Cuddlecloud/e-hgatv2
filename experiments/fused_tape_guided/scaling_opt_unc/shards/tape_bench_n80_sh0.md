# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.5119 ± 0.0000 | 1191.0109 ± 0.0000 | 1678.7984 ± 0.0000 | 1.0656 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.6386 ± 0.0000 | 1012.5884 ± 0.0000 | 934.7037 ± 0.0000 | 0.8999 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.0714 ± 0.0000 | 3593.4849 ± 0.0000 | 4660.9582 ± 0.0000 | 0.8721 ± 0.0000 | 65600 |
| mp-BRKGA | 0.3561 ± 0.0000 | 2205.9622 ± 0.0000 | 1318.2758 ± 0.0000 | 0.8302 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.0659 ± 0.0000 | 4166.4883 ± 0.0000 | 4452.2998 ± 0.0000 | 0.8132 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

