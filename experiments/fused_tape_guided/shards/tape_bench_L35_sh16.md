# Faithful-guidance study -- L35 (N=12, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 60x4 = GAT/BRKGA 240/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9481 ± 0.0507 | 7.5736 ± 8.7822 | 9.7059 ± 8.6706 | 0.7795 ± 0.0912 | 9840 |
| E-HGATv2-attn | 0.9493 ± 0.0291 | 4.6842 ± 3.1764 | 7.8771 ± 3.5724 | 0.8554 ± 0.1150 | 9840 |
| NSGA-II (random) | 0.8397 ± 0.0454 | 30.6473 ± 15.4461 | 34.9714 ± 17.0462 | 0.8753 ± 0.1756 | 9840 |
| mp-BRKGA | 0.7819 ± 0.1082 | 60.8725 ± 9.8832 | 47.2344 ± 22.4665 | 0.8265 ± 0.1864 | 9840 |
| single-pop BRKGA | 0.8742 ± 0.0488 | 15.6484 ± 6.7103 | 31.7643 ± 15.7164 | 0.9350 ± 0.2912 | 9840 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.084 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.989** |
| random baseline | 0.083 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 7.821. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

