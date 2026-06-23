# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_5 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9312 ± 0.1614 | 72.6976 ± 96.1483 | 114.6340 ± 172.4193 | 0.9389 ± 0.0750 | 16400 |
| E-HGATv2-attn | 0.9566 ± 0.1159 | 64.3272 ± 47.4123 | 79.3841 ± 57.8329 | 0.8783 ± 0.1087 | 16400 |
| NSGA-II (random) | 0.8095 ± 0.0879 | 156.0756 ± 106.7346 | 197.1745 ± 119.0206 | 0.8232 ± 0.0032 | 16400 |
| mp-BRKGA | 0.8904 ± 0.0708 | 485.9278 ± 406.7644 | 117.2894 ± 60.9359 | 0.9935 ± 0.1066 | 16400 |
| single-pop BRKGA | 0.8315 ± 0.0939 | 116.6146 ± 85.6841 | 186.2519 ± 123.6290 | 0.8784 ± 0.0758 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | 0.016 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.949** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 16.737. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

