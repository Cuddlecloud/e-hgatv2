# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8616 ± 0.0000 | 9.8646 ± 0.0000 | 1213.3626 ± 0.0000 | 0.8862 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7775 ± 0.0000 | 442.9521 ± 0.0000 | 1437.3273 ± 0.0000 | 0.7934 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.5749 ± 0.0000 | 625.0039 ± 0.0000 | 2926.0779 ± 0.0000 | 0.8913 ± 0.0000 | 16400 |
| mp-BRKGA | 0.8285 ± 0.0000 | 362.6975 ± 0.0000 | 503.5781 ± 0.0000 | 0.7678 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.4797 ± 0.0000 | 1092.1339 ± 0.0000 | 3669.5046 ± 0.0000 | 0.8684 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

