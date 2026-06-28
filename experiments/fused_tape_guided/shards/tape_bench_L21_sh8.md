# Faithful-guidance study -- L21 (N=12, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 60x4 = GAT/BRKGA 240/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9934 ± 0.0897 | 5.3871 ± 6.1364 | 6.9146 ± 4.9017 | 0.8958 ± 0.0650 | 9840 |
| E-HGATv2-attn | 0.9343 ± 0.0783 | 5.1764 ± 2.4039 | 5.6437 ± 3.2341 | 0.9319 ± 0.0655 | 9840 |
| NSGA-II (random) | 0.9308 ± 0.0488 | 7.1060 ± 4.8062 | 11.9893 ± 9.4918 | 0.9430 ± 0.0659 | 9840 |
| mp-BRKGA | 0.8631 ± 0.1687 | 32.7735 ± 37.2721 | 55.8782 ± 68.8510 | 0.8977 ± 0.1842 | 9840 |
| single-pop BRKGA | 0.9016 ± 0.1698 | 12.3321 ± 16.0096 | 21.7047 ± 17.2275 | 0.9160 ± 0.0806 | 9840 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.054 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.988** |
| random baseline | 0.083 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 2.184. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

