# Faithful-guidance study -- L15 (N=16, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 80x4 = GAT/BRKGA 320/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9306 ± 0.0507 | 15.0753 ± 3.8348 | 14.9340 ± 4.8389 | 0.8473 ± 0.1210 | 13120 |
| E-HGATv2-attn | 0.8628 ± 0.0496 | 27.8653 ± 26.8948 | 25.1594 ± 16.1083 | 0.8694 ± 0.0499 | 13120 |
| NSGA-II (random) | 0.8169 ± 0.1110 | 43.9167 ± 22.3303 | 42.8235 ± 19.2542 | 0.8214 ± 0.0921 | 13120 |
| mp-BRKGA | 0.6592 ± 0.1759 | 158.5902 ± 164.3474 | 88.5103 ± 41.0679 | 0.7869 ± 0.1711 | 13120 |
| single-pop BRKGA | 0.7818 ± 0.0506 | 52.0439 ± 4.7736 | 45.3279 ± 4.3254 | 0.8518 ± 0.1352 | 13120 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | 0.064 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.996** |
| random baseline | 0.062 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 3.289. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

