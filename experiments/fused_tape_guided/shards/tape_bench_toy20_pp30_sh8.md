# Faithful-guidance study -- toy:20 (N=20, coupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.6769 ± 0.2229 | 180.3793 ± 70.5118 | 206.3394 ± 186.3325 | 0.9323 ± 0.1225 | 16400 |
| E-HGATv2-attn | 0.6902 ± 0.1730 | 106.6019 ± 16.9428 | 145.7964 ± 78.0972 | 1.0027 ± 0.2345 | 16400 |
| NSGA-II (random) | 0.3276 ± 0.0873 | 356.5763 ± 126.0188 | 512.3081 ± 135.4528 | 0.8708 ± 0.1536 | 16400 |
| mp-BRKGA | 0.5323 ± 0.1777 | 306.2496 ± 204.3489 | 178.4062 ± 129.0149 | 1.0717 ± 0.2725 | 16400 |
| single-pop BRKGA | 0.4341 ± 0.1809 | 264.9216 ± 116.4515 | 359.6309 ± 203.4135 | 0.7924 ± 0.1081 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.046 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.848** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 56.139. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

