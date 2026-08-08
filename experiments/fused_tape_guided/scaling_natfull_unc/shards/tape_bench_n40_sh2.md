# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7976 ± 0.0000 | 80.9068 ± 0.0000 | 344.7218 ± 0.0000 | 0.8472 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.9767 ± 0.0000 | 17.6265 ± 0.0000 | 21.8796 ± 0.0000 | 0.8623 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.5978 ± 0.0000 | 239.2355 ± 0.0000 | 626.4611 ± 0.0000 | 0.8802 ± 0.0000 | 32800 |
| mp-BRKGA | 0.7875 ± 0.0000 | 240.9846 ± 0.0000 | 149.6154 ± 0.0000 | 0.7042 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.4121 ± 0.0000 | 711.8142 ± 0.0000 | 1020.1601 ± 0.0000 | 0.9442 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

