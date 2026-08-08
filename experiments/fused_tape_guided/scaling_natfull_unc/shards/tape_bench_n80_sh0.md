# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8438 ± 0.0000 | 77.7761 ± 0.0000 | 858.3004 ± 0.0000 | 0.8472 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.7963 ± 0.0000 | 110.9218 ± 0.0000 | 1278.4220 ± 0.0000 | 0.8300 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.6003 ± 0.0000 | 663.5030 ± 0.0000 | 2563.4379 ± 0.0000 | 0.8217 ± 0.0000 | 65600 |
| mp-BRKGA | 0.8892 ± 0.0000 | 197.1835 ± 0.0000 | 268.3690 ± 0.0000 | 0.7406 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.5559 ± 0.0000 | 1055.2234 ± 0.0000 | 2500.4905 ± 0.0000 | 0.7294 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

