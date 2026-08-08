# Faithful-guidance study -- toy:8 (N=8, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 40x4 = GAT/BRKGA 160/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9322 ± 0.0670 | 20.7423 ± 13.9053 | 57.7423 ± 72.3604 | 0.9810 ± 0.1305 | 6560 |
| E-HGATv2-attn | 0.9619 ± 0.0225 | 17.7544 ± 8.2696 | 17.9907 ± 7.1215 | 1.0280 ± 0.1324 | 6560 |
| NSGA-II (random) | 0.9252 ± 0.0319 | 29.7926 ± 41.4111 | 45.7437 ± 37.2663 | 0.9796 ± 0.3268 | 6560 |
| mp-BRKGA | 0.8755 ± 0.0465 | 41.3468 ± 22.7588 | 85.0017 ± 69.4027 | 0.8405 ± 0.2610 | 6560 |
| single-pop BRKGA | 0.8963 ± 0.0371 | 22.5101 ± 13.2323 | 74.9077 ± 47.1191 | 0.9598 ± 0.0651 | 6560 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.800 | -0.023 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.990** |
| random baseline | 0.125 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 8.978. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

