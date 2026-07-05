# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8460 ± 0.0000 | 347.4624 ± 0.0000 | 274.9236 ± 0.0000 | 0.9457 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.8268 ± 0.0000 | 321.3650 ± 0.0000 | 263.6254 ± 0.0000 | 0.9379 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.5053 ± 0.0000 | 560.1361 ± 0.0000 | 1303.9896 ± 0.0000 | 0.9341 ± 0.0000 | 32800 |
| mp-BRKGA | 0.9283 ± 0.0000 | 374.8499 ± 0.0000 | 105.1210 ± 0.0000 | 0.9875 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.3955 ± 0.0000 | 808.4811 ± 0.0000 | 1808.9925 ± 0.0000 | 0.8139 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

