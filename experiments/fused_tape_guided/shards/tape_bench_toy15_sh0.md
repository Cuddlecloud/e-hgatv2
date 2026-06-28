# Faithful-guidance study -- toy:15 (N=15, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 75x4 = GAT/BRKGA 300/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9431 ± 0.0739 | 44.9477 ± 39.4745 | 51.0068 ± 41.8106 | 0.9269 ± 0.2015 | 12300 |
| E-HGATv2-attn | 0.9352 ± 0.0287 | 44.5770 ± 19.8103 | 46.6652 ± 17.4129 | 0.8774 ± 0.1765 | 12300 |
| NSGA-II (random) | 0.8280 ± 0.0763 | 104.7190 ± 62.1032 | 136.2767 ± 103.6837 | 0.8977 ± 0.1037 | 12300 |
| mp-BRKGA | 0.7990 ± 0.0359 | 164.3313 ± 145.2774 | 130.4072 ± 24.1078 | 0.9418 ± 0.1190 | 12300 |
| single-pop BRKGA | 0.8559 ± 0.0760 | 66.6747 ± 64.1836 | 119.4592 ± 142.9497 | 0.9127 ± 0.2156 | 12300 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.800 | 0.081 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.067 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.749. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

