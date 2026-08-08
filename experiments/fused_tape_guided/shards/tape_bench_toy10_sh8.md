# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8655 ± 0.1223 | 48.3014 ± 92.9877 | 96.3491 ± 84.5694 | 0.9117 ± 0.0646 | 8200 |
| E-HGATv2-attn | 0.9130 ± 0.1004 | 31.1083 ± 26.0922 | 36.7469 ± 61.1268 | 1.0012 ± 0.2264 | 8200 |
| NSGA-II (random) | 0.8275 ± 0.1843 | 61.0917 ± 69.9675 | 114.7669 ± 141.9289 | 0.8857 ± 0.1184 | 8200 |
| mp-BRKGA | 0.7575 ± 0.0451 | 270.0921 ± 246.0706 | 131.2102 ± 76.2459 | 0.9616 ± 0.1759 | 8200 |
| single-pop BRKGA | 0.7569 ± 0.1301 | 109.8108 ± 107.4666 | 158.2996 ± 107.2350 | 0.8440 ± 0.0877 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

