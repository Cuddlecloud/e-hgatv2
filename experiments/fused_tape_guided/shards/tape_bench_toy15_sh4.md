# Faithful-guidance study -- toy:15 (N=15, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 75x4 = GAT/BRKGA 300/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9327 ± 0.0833 | 28.3472 ± 43.3629 | 62.0670 ± 63.0841 | 0.9130 ± 0.1396 | 12300 |
| E-HGATv2-attn | 0.8899 ± 0.0472 | 48.0519 ± 19.9109 | 87.1197 ± 37.4909 | 0.8686 ± 0.1568 | 12300 |
| NSGA-II (random) | 0.8193 ± 0.0231 | 91.0348 ± 33.1603 | 160.4597 ± 41.2160 | 0.8644 ± 0.1377 | 12300 |
| mp-BRKGA | 0.7991 ± 0.1398 | 160.0159 ± 174.3742 | 177.3491 ± 129.4832 | 0.9372 ± 0.0785 | 12300 |
| single-pop BRKGA | 0.7986 ± 0.0916 | 83.9403 ± 95.1924 | 183.8024 ± 123.0812 | 0.9250 ± 0.1086 | 12300 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.800 | 0.081 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.067 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.749. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

