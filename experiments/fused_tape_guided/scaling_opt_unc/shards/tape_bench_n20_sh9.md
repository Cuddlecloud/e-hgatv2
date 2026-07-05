# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8297 ± 0.0000 | 177.2888 ± 0.0000 | 181.5182 ± 0.0000 | 1.0289 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.8606 ± 0.0000 | 115.2749 ± 0.0000 | 141.8314 ± 0.0000 | 0.9649 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.7471 ± 0.0000 | 304.4782 ± 0.0000 | 290.7178 ± 0.0000 | 1.0084 ± 0.0000 | 16400 |
| mp-BRKGA | 0.7082 ± 0.0000 | 698.8050 ± 0.0000 | 392.1554 ± 0.0000 | 0.9409 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.6248 ± 0.0000 | 369.1982 ± 0.0000 | 590.3182 ± 0.0000 | 0.8115 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

