# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8337 ± 0.0000 | 354.2446 ± 0.0000 | 557.9254 ± 0.0000 | 0.8305 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.7716 ± 0.0000 | 420.8790 ± 0.0000 | 440.5972 ± 0.0000 | 0.8395 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.1623 ± 0.0000 | 2165.1618 ± 0.0000 | 4701.8509 ± 0.0000 | 0.7939 ± 0.0000 | 131200 |
| mp-BRKGA | 0.1141 ± 0.0000 | 2758.6124 ± 0.0000 | 3858.4432 ± 0.0000 | 0.8595 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.1090 ± 0.0000 | 2312.6134 ± 0.0000 | 5136.9538 ± 0.0000 | 0.8059 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

