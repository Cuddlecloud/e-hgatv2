# Faithful-guidance study -- toy:40 (N=40, coupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.7652 ± 0.0000 | 46.5288 ± 0.0000 | 527.9779 ± 0.0000 | 0.7596 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.8711 ± 0.0000 | 795.0299 ± 0.0000 | 305.8735 ± 0.0000 | 0.9689 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.4788 ± 0.0000 | 612.6724 ± 0.0000 | 1175.6444 ± 0.0000 | 0.8687 ± 0.0000 | 32800 |
| mp-BRKGA | 0.8636 ± 0.0000 | 293.3932 ± 0.0000 | 202.5345 ± 0.0000 | 0.7313 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.4541 ± 0.0000 | 846.5166 ± 0.0000 | 1229.8928 ± 0.0000 | 0.7348 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.633 | -0.003 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.902** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 75.981. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

