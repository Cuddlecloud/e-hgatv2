# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8036 ± 0.0000 | 140.8690 ± 0.0000 | 180.1597 ± 0.0000 | 0.9943 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7239 ± 0.0000 | 170.6120 ± 0.0000 | 200.5885 ± 0.0000 | 0.9076 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.6996 ± 0.0000 | 165.8033 ± 0.0000 | 198.9827 ± 0.0000 | 0.7397 ± 0.0000 | 16400 |
| mp-BRKGA | 0.5780 ± 0.0000 | 418.5191 ± 0.0000 | 269.3476 ± 0.0000 | 0.8724 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.4951 ± 0.0000 | 511.4885 ± 0.0000 | 398.5778 ± 0.0000 | 0.8540 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

