# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8223 ± 0.0424 | 79.6844 ± 32.6090 | 117.8040 ± 18.7216 | 0.8611 ± 0.0932 | 16400 |
| E-HGATv2-attn | 0.7409 ± 0.0457 | 101.7316 ± 49.9338 | 140.0485 ± 54.1401 | 0.8534 ± 0.0848 | 16400 |
| NSGA-II (random) | 0.5433 ± 0.1243 | 297.8920 ± 74.5609 | 319.4529 ± 172.5885 | 0.8285 ± 0.2656 | 16400 |
| mp-BRKGA | 0.6307 ± 0.2233 | 588.8821 ± 349.1928 | 205.7384 ± 163.3245 | 0.9534 ± 0.0642 | 16400 |
| single-pop BRKGA | 0.5330 ± 0.1707 | 270.8568 ± 158.3032 | 346.1525 ± 157.1591 | 0.8610 ± 0.1038 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

