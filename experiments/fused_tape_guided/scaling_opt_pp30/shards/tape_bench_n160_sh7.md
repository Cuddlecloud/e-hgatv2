# Faithful-guidance study -- toy:160 (N=160, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 800x4 = GAT/BRKGA 3200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9382 ± 0.0000 | 212.8490 ± 0.0000 | 258.5152 ± 0.0000 | 0.8943 ± 0.0000 | 131200 |
| E-HGATv2-attn | 0.9001 ± 0.0000 | 410.0364 ± 0.0000 | 395.8298 ± 0.0000 | 0.6931 ± 0.0000 | 131200 |
| NSGA-II (random) | 0.2685 ± 0.0000 | 2248.8637 ± 0.0000 | 5271.1001 ± 0.0000 | 0.8682 ± 0.0000 | 131200 |
| mp-BRKGA | 0.3186 ± 0.0000 | 2136.7097 ± 0.0000 | 4092.6417 ± 0.0000 | 0.7384 ± 0.0000 | 131200 |
| single-pop BRKGA | 0.2481 ± 0.0000 | 2540.9747 ± 0.0000 | 4919.4861 ± 0.0000 | 0.7709 ± 0.0000 | 131200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.001 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.909** |
| random baseline | 0.006 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 196.202. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

