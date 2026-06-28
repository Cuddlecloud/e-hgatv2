# Faithful-guidance study -- L07 (N=8, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 40x4 = GAT/BRKGA 160/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9786 ± 0.0434 | 1.8119 ± 2.9754 | 19.3480 ± 31.1641 | 0.8166 ± 0.0937 | 6560 |
| E-HGATv2-attn | 0.9666 ± 0.0302 | 0.8409 ± 0.8626 | 28.1457 ± 28.1503 | 0.8312 ± 0.0283 | 6560 |
| NSGA-II (random) | 0.9424 ± 0.0324 | 10.2037 ± 8.4761 | 32.1285 ± 29.4194 | 0.9048 ± 0.0597 | 6560 |
| mp-BRKGA | 0.9342 ± 0.0343 | 21.3842 ± 11.0763 | 36.3967 ± 29.8798 | 0.7868 ± 0.1180 | 6560 |
| single-pop BRKGA | 0.9349 ± 0.0602 | 9.4101 ± 12.2583 | 34.4894 ± 42.2240 | 0.8861 ± 0.1477 | 6560 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.867 | 0.176 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.985** |
| random baseline | 0.125 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 2.221. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

