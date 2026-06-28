# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8997 ± 0.1182 | 338.2683 ± 837.3840 | 96.9928 ± 82.7724 | 0.9134 ± 0.1134 | 16400 |
| E-HGATv2-attn | 0.8849 ± 0.1982 | 62.4927 ± 90.5263 | 110.9024 ± 115.7908 | 0.8564 ± 0.1047 | 16400 |
| NSGA-II (random) | 0.7132 ± 0.0694 | 213.8489 ± 68.4892 | 254.0072 ± 114.4849 | 0.7699 ± 0.1439 | 16400 |
| mp-BRKGA | 0.7662 ± 0.1508 | 698.5942 ± 156.3084 | 179.7935 ± 120.7518 | 1.0067 ± 0.0731 | 16400 |
| single-pop BRKGA | 0.7526 ± 0.1739 | 222.0145 ± 36.0138 | 211.5377 ± 184.1125 | 0.8669 ± 0.1150 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

