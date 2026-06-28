# Faithful-guidance study -- toy:8 (N=8, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 40x4 = GAT/BRKGA 160/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9379 ± 0.0176 | 16.1594 ± 13.7203 | 34.7690 ± 8.5679 | 0.9333 ± 0.0583 | 6560 |
| E-HGATv2-attn | 0.9680 ± 0.0312 | 6.6381 ± 8.3465 | 17.4433 ± 19.5435 | 1.0054 ± 0.1372 | 6560 |
| NSGA-II (random) | 0.9414 ± 0.0272 | 13.6429 ± 10.5049 | 29.8110 ± 22.2968 | 1.0012 ± 0.0927 | 6560 |
| mp-BRKGA | 0.9159 ± 0.0313 | 27.8626 ± 13.9768 | 49.0499 ± 22.4775 | 0.8339 ± 0.1401 | 6560 |
| single-pop BRKGA | 0.9183 ± 0.0377 | 13.3306 ± 6.0143 | 47.0761 ± 14.2379 | 0.9673 ± 0.0909 | 6560 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.800 | -0.023 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.990** |
| random baseline | 0.125 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 8.978. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

