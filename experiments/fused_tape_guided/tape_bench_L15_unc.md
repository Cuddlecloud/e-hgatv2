# Faithful-guidance study -- L15 (N=16, uncoupled)

_5 seeds, 40 gens, matched exact-eval budget (mp 80x4 = GAT/BRKGA 320/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9587 ± 0.0257 | 31.9184 ± 29.3901 | 19.6319 ± 11.8170 | 0.8114 ± 0.1082 | 13120 |
| E-HGATv2-attn | 0.9532 ± 0.0194 | 26.5663 ± 16.5067 | 20.1118 ± 7.2913 | 0.9149 ± 0.2265 | 13120 |
| NSGA-II (random) | 0.8940 ± 0.0337 | 55.9074 ± 13.9338 | 48.9083 ± 17.0627 | 0.7602 ± 0.0624 | 13120 |
| mp-BRKGA | 0.8739 ± 0.0169 | 259.1640 ± 113.7448 | 67.8245 ± 11.2571 | 0.7988 ± 0.1120 | 13120 |
| single-pop BRKGA | 0.8912 ± 0.0283 | 62.6101 ± 34.7420 | 48.8462 ± 16.4112 | 0.8021 ± 0.1089 | 13120 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | 0.081 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.996** |
| random baseline | 0.062 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 2.782. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

