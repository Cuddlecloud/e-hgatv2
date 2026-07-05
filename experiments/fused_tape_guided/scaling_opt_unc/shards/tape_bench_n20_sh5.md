# Faithful-guidance study -- toy:20 (N=20, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8760 ± 0.0000 | 78.2742 ± 0.0000 | 131.7357 ± 0.0000 | 0.8702 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7758 ± 0.0000 | 144.8996 ± 0.0000 | 151.2335 ± 0.0000 | 0.9761 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.7470 ± 0.0000 | 146.4903 ± 0.0000 | 192.2824 ± 0.0000 | 0.8802 ± 0.0000 | 16400 |
| mp-BRKGA | 0.6773 ± 0.0000 | 522.8026 ± 0.0000 | 198.2060 ± 0.0000 | 0.8289 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.5022 ± 0.0000 | 527.0907 ± 0.0000 | 352.0273 ± 0.0000 | 1.0073 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.952** |
| random baseline | 0.050 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.634. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

