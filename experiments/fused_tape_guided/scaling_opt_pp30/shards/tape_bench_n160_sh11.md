# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8576 ± 0.0000 | 474.7026 ± 0.0000 | 676.3907 ± 0.0000 | 0.8331 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.8237 ± 0.0000 | 667.8173 ± 0.0000 | 665.9678 ± 0.0000 | 1.0030 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.2804 ± 0.0000 | 2882.8264 ± 0.0000 | 5095.1487 ± 0.0000 | 0.8684 ± 0.0000 | 131200 |
| mp-BRKGA | 0.3442 ± 0.0000 | 2448.7034 ± 0.0000 | 3883.6971 ± 0.0000 | 0.8618 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.2705 ± 0.0000 | 2411.8220 ± 0.0000 | 4906.6557 ± 0.0000 | 0.8110 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

