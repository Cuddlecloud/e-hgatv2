# Faithful-guidance study -- L07 (N=8, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 40x4 = GAT/BRKGA 160/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9719 ± 0.0405 | 2.0889 ± 1.2477 | 20.9665 ± 31.4203 | 0.8344 ± 0.1435 | 6560 |
| E-HGATv2-attn | 0.9645 ± 0.0297 | 2.2061 ± 3.1303 | 23.2420 ± 31.9697 | 0.8491 ± 0.1120 | 6560 |
| NSGA-II (random) | 0.9589 ± 0.0388 | 5.1638 ± 3.1521 | 21.3661 ± 30.4506 | 0.9127 ± 0.0647 | 6560 |
| mp-BRKGA | 0.9386 ± 0.0340 | 22.5413 ± 15.6818 | 30.5235 ± 26.8473 | 0.7872 ± 0.1048 | 6560 |
| single-pop BRKGA | 0.9451 ± 0.0279 | 8.2002 ± 5.7209 | 29.7782 ± 31.5624 | 0.8956 ± 0.0887 | 6560 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.867 | 0.176 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.985** |
| random baseline | 0.125 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 2.221. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

