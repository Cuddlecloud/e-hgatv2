# Faithful-guidance study -- L21 (N=12, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 60x4 = GAT/BRKGA 240/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9481 ± 0.0505 | 7.3849 ± 12.9781 | 8.8606 ± 12.6253 | 0.7896 ± 0.1661 | 9840 |
| E-HGATv2-attn | 0.9055 ± 0.0256 | 6.8481 ± 6.5161 | 10.8704 ± 5.5092 | 0.9531 ± 0.0543 | 9840 |
| NSGA-II (random) | 0.8864 ± 0.0254 | 13.0119 ± 7.1056 | 15.7861 ± 6.5065 | 0.8469 ± 0.2223 | 9840 |
| mp-BRKGA | 0.7563 ± 0.1205 | 77.1495 ± 77.2538 | 48.6826 ± 23.2498 | 0.8749 ± 0.2754 | 9840 |
| single-pop BRKGA | 0.8615 ± 0.0433 | 20.4087 ± 6.9757 | 23.7605 ± 8.9354 | 0.8839 ± 0.0755 | 9840 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.054 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.988** |
| random baseline | 0.083 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 2.184. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

