# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.6716 ± 0.0000 | 1033.7910 ± 0.0000 | 871.9906 ± 0.0000 | 0.8326 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.5901 ± 0.0000 | 830.2443 ± 0.0000 | 1083.1345 ± 0.0000 | 0.8684 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.0952 ± 0.0000 | 3473.1381 ± 0.0000 | 4611.4957 ± 0.0000 | 0.8644 ± 0.0000 | 65600 |
| mp-BRKGA | 0.3480 ± 0.0000 | 3179.0246 ± 0.0000 | 1381.2163 ± 0.0000 | 0.7970 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.0240 ± 0.0000 | 2935.3050 ± 0.0000 | 5258.7825 ± 0.0000 | 0.9258 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

