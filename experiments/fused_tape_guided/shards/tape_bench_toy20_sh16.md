# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8854 ± 0.1671 | 92.8516 ± 133.1019 | 97.8820 ± 126.2613 | 0.8650 ± 0.0672 | 16400 |
| E-HGATv2-attn | 0.9355 ± 0.0809 | 128.3341 ± 60.9359 | 57.9255 ± 46.1145 | 0.9312 ± 0.0602 | 16400 |
| NSGA-II (random) | 0.6795 ± 0.0878 | 267.7663 ± 107.2999 | 288.6133 ± 123.4262 | 0.8554 ± 0.1180 | 16400 |
| mp-BRKGA | 0.8163 ± 0.1254 | 504.5420 ± 474.4923 | 144.1564 ± 65.0780 | 0.9115 ± 0.0711 | 16400 |
| single-pop BRKGA | 0.7790 ± 0.1920 | 165.6257 ± 203.2596 | 194.8472 ± 152.4520 | 0.8635 ± 0.0970 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

