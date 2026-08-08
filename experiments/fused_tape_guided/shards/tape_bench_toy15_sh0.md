# Faithful-guidance study -- toy:15 (N=15, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 75x4 = GAT/BRKGA 300/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8645 ± 0.0948 | 77.1112 ± 90.9735 | 95.4985 ± 108.9406 | 1.0410 ± 0.0556 | 12300 |
| E-HGATv2-attn | 0.8942 ± 0.0416 | 49.7340 ± 16.3110 | 66.2856 ± 35.4287 | 0.8995 ± 0.1408 | 12300 |
| NSGA-II (random) | 0.7622 ± 0.1114 | 128.7284 ± 104.9962 | 255.0184 ± 226.9843 | 0.9145 ± 0.1182 | 12300 |
| mp-BRKGA | 0.7431 ± 0.0312 | 180.6609 ± 144.2247 | 151.4332 ± 43.5459 | 0.9459 ± 0.1201 | 12300 |
| single-pop BRKGA | 0.7949 ± 0.0271 | 89.0426 ± 28.9825 | 169.2908 ± 115.2067 | 0.9015 ± 0.1492 | 12300 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.800 | 0.081 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.067 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.749. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

