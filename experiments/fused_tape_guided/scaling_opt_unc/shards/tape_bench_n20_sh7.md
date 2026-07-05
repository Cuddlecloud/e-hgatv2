# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8854 ± 0.0000 | 72.8156 ± 0.0000 | 199.1101 ± 0.0000 | 0.9050 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.9145 ± 0.0000 | 84.0183 ± 0.0000 | 167.5052 ± 0.0000 | 0.8916 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.6941 ± 0.0000 | 285.5325 ± 0.0000 | 510.2506 ± 0.0000 | 0.9914 ± 0.0000 | 16400 |
| mp-BRKGA | 0.7954 ± 0.0000 | 407.1326 ± 0.0000 | 330.5311 ± 0.0000 | 1.0646 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.5958 ± 0.0000 | 360.9062 ± 0.0000 | 780.7737 ± 0.0000 | 0.9403 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

