# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8284 ± 0.0000 | 115.1185 ± 0.0000 | 101.1837 ± 0.0000 | 1.0351 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.8901 ± 0.0000 | 51.4015 ± 0.0000 | 43.0200 ± 0.0000 | 1.0677 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.7205 ± 0.0000 | 181.0228 ± 0.0000 | 182.5866 ± 0.0000 | 0.8819 ± 0.0000 | 8200 |
| mp-BRKGA | 0.6926 ± 0.0000 | 305.4317 ± 0.0000 | 139.4596 ± 0.0000 | 0.8725 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.8228 ± 0.0000 | 83.6369 ± 0.0000 | 102.6749 ± 0.0000 | 0.8831 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

