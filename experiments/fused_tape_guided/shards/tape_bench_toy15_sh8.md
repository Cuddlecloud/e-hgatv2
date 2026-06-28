# Faithful-guidance study -- toy:15 (N=15, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 75x4 = GAT/BRKGA 300/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9152 ± 0.0485 | 37.3351 ± 14.3042 | 72.1212 ± 69.5748 | 0.9293 ± 0.0657 | 12300 |
| E-HGATv2-attn | 0.9240 ± 0.0445 | 28.9055 ± 32.7709 | 63.9781 ± 52.3295 | 0.9286 ± 0.0772 | 12300 |
| NSGA-II (random) | 0.8445 ± 0.0409 | 87.0651 ± 52.3237 | 101.7037 ± 29.9778 | 0.8980 ± 0.1218 | 12300 |
| mp-BRKGA | 0.8539 ± 0.0381 | 97.2016 ± 56.0030 | 100.3308 ± 29.7462 | 0.8875 ± 0.1197 | 12300 |
| single-pop BRKGA | 0.8143 ± 0.0551 | 90.8528 ± 57.0327 | 149.6407 ± 46.9277 | 0.8054 ± 0.1881 | 12300 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.800 | 0.081 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.067 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.749. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

