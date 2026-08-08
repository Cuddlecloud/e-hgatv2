# Faithful-guidance study -- L21 (N=12, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 60x4 = GAT/BRKGA 240/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9727 ± 0.0224 | 4.8072 ± 3.0098 | 4.8296 ± 1.6227 | 0.9076 ± 0.1581 | 9840 |
| E-HGATv2-attn | 0.9498 ± 0.0249 | 4.8910 ± 1.5210 | 6.1020 ± 1.7455 | 0.9207 ± 0.1288 | 9840 |
| NSGA-II (random) | 0.8812 ± 0.0472 | 15.7850 ± 14.7606 | 16.9498 ± 11.4389 | 0.9082 ± 0.1093 | 9840 |
| mp-BRKGA | 0.7588 ± 0.1247 | 78.3573 ± 65.6032 | 76.9214 ± 68.0379 | 0.9263 ± 0.1364 | 9840 |
| single-pop BRKGA | 0.8992 ± 0.0717 | 19.9149 ± 23.8394 | 24.6244 ± 24.1958 | 0.8555 ± 0.0645 | 9840 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.054 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.988** |
| random baseline | 0.083 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 2.184. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

