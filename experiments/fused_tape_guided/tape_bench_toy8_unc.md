# Faithful-guidance study -- toy:8 (N=8, uncoupled)

_5 seeds, 40 gens, matched exact-eval budget (mp 40x4 = GAT/BRKGA 160/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9418 ± 0.0341 | 23.2004 ± 23.7631 | 49.4046 ± 31.1691 | 0.9452 ± 0.0154 | 6560 |
| E-HGATv2-attn | 0.9611 ± 0.0255 | 14.0407 ± 12.5831 | 24.1963 ± 26.6417 | 0.9563 ± 0.0789 | 6560 |
| NSGA-II (random) | 0.9236 ± 0.0224 | 23.2190 ± 16.5584 | 49.7176 ± 29.9895 | 0.9455 ± 0.1087 | 6560 |
| mp-BRKGA | 0.9023 ± 0.0169 | 31.6282 ± 16.1001 | 72.9011 ± 9.7000 | 0.8627 ± 0.1096 | 6560 |
| single-pop BRKGA | 0.9051 ± 0.0231 | 13.5048 ± 5.7266 | 71.6835 ± 44.4731 | 0.9918 ± 0.0984 | 6560 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.800 | -0.008 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.990** |
| random baseline | 0.125 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 9.085. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

