# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9622 ± 0.0000 | 39.8215 ± 0.0000 | 13.6012 ± 0.0000 | 0.9413 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.8819 ± 0.0000 | 35.1740 ± 0.0000 | 49.1839 ± 0.0000 | 0.9816 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.8628 ± 0.0000 | 51.6586 ± 0.0000 | 42.3823 ± 0.0000 | 0.9095 ± 0.0000 | 8200 |
| mp-BRKGA | 0.6569 ± 0.0000 | 403.1191 ± 0.0000 | 148.5396 ± 0.0000 | 0.9315 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8076 ± 0.0000 | 78.7922 ± 0.0000 | 71.0303 ± 0.0000 | 0.8753 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

