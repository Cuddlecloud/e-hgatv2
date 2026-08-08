# Faithful-guidance study -- toy:8 (N=8, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 40x4 = GAT/BRKGA 160/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9574 ± 0.0324 | 22.1294 ± 22.9643 | 24.1485 ± 27.0155 | 0.9914 ± 0.0938 | 6560 |
| E-HGATv2-attn | 0.9590 ± 0.0391 | 10.2487 ± 4.9870 | 17.0696 ± 16.8318 | 0.9177 ± 0.1231 | 6560 |
| NSGA-II (random) | 0.9166 ± 0.0404 | 23.9709 ± 5.5977 | 40.1433 ± 26.8459 | 0.8367 ± 0.1293 | 6560 |
| mp-BRKGA | 0.8846 ± 0.0373 | 37.7562 ± 40.0362 | 58.2685 ± 35.8584 | 0.9048 ± 0.1192 | 6560 |
| single-pop BRKGA | 0.9127 ± 0.0178 | 17.8103 ± 22.5143 | 39.5265 ± 9.4202 | 1.0055 ± 0.1497 | 6560 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.800 | -0.023 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.990** |
| random baseline | 0.125 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 8.978. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

