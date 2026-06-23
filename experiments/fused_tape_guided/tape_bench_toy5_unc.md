# Faithful-guidance study -- toy:5 (N=5, uncoupled)

_5 seeds, 40 gens, matched exact-eval budget (mp 25x4 = GAT/BRKGA 100/gen). Reference: exact Oracle. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9779 ± 0.0304 | 1.3830 ± 0.9835 | 17.1673 ± 25.7012 | 0.9114 ± 0.0733 | 4100 |
| E-HGATv2-attn | 0.9649 ± 0.0349 | 0.6158 ± 0.5671 | 19.3183 ± 26.8173 | 0.9591 ± 0.0587 | 4100 |
| NSGA-II (random) | 0.9809 ± 0.0093 | 1.7263 ± 1.1838 | 5.5797 ± 2.9443 | 0.9418 ± 0.0659 | 4100 |
| mp-BRKGA | 0.9341 ± 0.0325 | 14.0438 ± 6.5608 | 39.8162 ± 27.1889 | 0.7635 ± 0.0466 | 4100 |
| single-pop BRKGA | 0.9758 ± 0.0167 | 3.2158 ± 1.9191 | 12.8886 ± 18.7792 | 0.8436 ± 0.0970 | 4100 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.070 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.980** |
| random baseline | 0.200 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 7.631. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

