# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8886 ± 0.0947 | 98.6597 ± 102.1131 | 109.2235 ± 105.6404 | 0.8993 ± 0.1603 | 16400 |
| E-HGATv2-attn | 0.8318 ± 0.0597 | 110.8891 ± 74.8988 | 173.1011 ± 80.2154 | 0.9808 ± 0.2136 | 16400 |
| NSGA-II (random) | 0.7508 ± 0.0466 | 184.4597 ± 47.1406 | 287.2086 ± 142.6520 | 0.8601 ± 0.0313 | 16400 |
| mp-BRKGA | 0.8043 ± 0.0582 | 137.5051 ± 64.8382 | 175.8810 ± 82.5635 | 0.9572 ± 0.1359 | 16400 |
| single-pop BRKGA | 0.7861 ± 0.1134 | 156.3203 ± 146.5688 | 254.8678 ± 176.2039 | 0.9172 ± 0.0714 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

