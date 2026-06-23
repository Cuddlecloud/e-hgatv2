# Faithful-guidance study -- L21 (N=12, uncoupled)

_5 seeds, 40 gens, matched exact-eval budget (mp 60x4 = GAT/BRKGA 240/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 1.0138 ± 0.0505 | 3.6600 ± 3.4371 | 3.4768 ± 1.4046 | 0.8779 ± 0.0759 | 9840 |
| E-HGATv2-attn | 0.9846 ± 0.0134 | 5.1947 ± 7.6546 | 6.4366 ± 8.4372 | 0.9087 ± 0.0633 | 9840 |
| NSGA-II (random) | 0.9380 ± 0.0289 | 9.8836 ± 7.5550 | 10.9135 ± 6.9087 | 0.9361 ± 0.0528 | 9840 |
| mp-BRKGA | 0.8415 ± 0.0766 | 51.5292 ± 33.8151 | 64.6976 ± 51.0997 | 0.9667 ± 0.1100 | 9840 |
| single-pop BRKGA | 0.9549 ± 0.0638 | 15.8854 ± 15.2463 | 23.6494 ± 17.8068 | 0.9353 ± 0.1104 | 9840 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.057 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.988** |
| random baseline | 0.083 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 2.358. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

