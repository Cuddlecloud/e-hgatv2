# Faithful-guidance study -- L35 (N=12, uncoupled)

_5 seeds, 40 gens, matched exact-eval budget (mp 60x4 = GAT/BRKGA 240/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9859 ± 0.0369 | 5.0366 ± 4.7279 | 9.4165 ± 10.2161 | 0.8651 ± 0.0800 | 9840 |
| E-HGATv2-attn | 0.9928 ± 0.0090 | 2.5316 ± 1.2465 | 4.3228 ± 0.7494 | 0.8619 ± 0.0711 | 9840 |
| NSGA-II (random) | 0.9436 ± 0.0274 | 17.0645 ± 10.2402 | 25.1800 ± 20.7081 | 0.9212 ± 0.1041 | 9840 |
| mp-BRKGA | 0.9303 ± 0.0422 | 36.2235 ± 20.4221 | 42.2446 ± 24.2453 | 0.8704 ± 0.1240 | 9840 |
| single-pop BRKGA | 0.9332 ± 0.0244 | 17.6242 ± 17.9403 | 27.7975 ± 19.1541 | 0.9293 ± 0.0954 | 9840 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.085 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **1.000** |
| random baseline | 0.083 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 6.649. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

