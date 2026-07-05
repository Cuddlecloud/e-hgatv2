# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8850 ± 0.0000 | 86.1811 ± 0.0000 | 170.2425 ± 0.0000 | 1.0525 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.8693 ± 0.0000 | 171.8848 ± 0.0000 | 199.3930 ± 0.0000 | 0.7951 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.4316 ± 0.0000 | 630.5979 ± 0.0000 | 1606.7390 ± 0.0000 | 0.9146 ± 0.0000 | 32800 |
| mp-BRKGA | 0.8084 ± 0.0000 | 357.9991 ± 0.0000 | 330.0144 ± 0.0000 | 0.9559 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.4472 ± 0.0000 | 823.0682 ± 0.0000 | 1398.8332 ± 0.0000 | 0.9164 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

