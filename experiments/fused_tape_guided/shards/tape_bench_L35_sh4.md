# Faithful-guidance study -- L35 (N=12, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 60x4 = GAT/BRKGA 240/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9527 ± 0.0261 | 12.4951 ± 10.3799 | 14.1738 ± 7.9051 | 0.7767 ± 0.2428 | 9840 |
| E-HGATv2-attn | 0.9652 ± 0.0299 | 7.5155 ± 6.8850 | 10.1213 ± 7.4915 | 0.8946 ± 0.1189 | 9840 |
| NSGA-II (random) | 0.8974 ± 0.0436 | 32.2305 ± 18.1771 | 40.7566 ± 35.9339 | 0.9055 ± 0.1510 | 9840 |
| mp-BRKGA | 0.8355 ± 0.0708 | 82.7786 ± 44.3429 | 74.8393 ± 42.2716 | 0.7855 ± 0.1601 | 9840 |
| single-pop BRKGA | 0.8905 ± 0.0187 | 28.5278 ± 31.3522 | 37.2135 ± 19.3325 | 0.9780 ± 0.2469 | 9840 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.084 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.989** |
| random baseline | 0.083 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 7.821. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

