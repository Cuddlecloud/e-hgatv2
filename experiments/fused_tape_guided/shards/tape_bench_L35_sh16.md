# Faithful-guidance study -- L35 (N=12, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 60x4 = GAT/BRKGA 240/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9749 ± 0.0262 | 6.3574 ± 5.7083 | 10.8580 ± 9.9500 | 0.8528 ± 0.1094 | 9840 |
| E-HGATv2-attn | 0.9715 ± 0.0305 | 11.6940 ± 8.9158 | 12.8612 ± 9.6326 | 0.9039 ± 0.1326 | 9840 |
| NSGA-II (random) | 0.9447 ± 0.0692 | 20.1664 ± 23.3483 | 25.9120 ± 28.3072 | 0.8753 ± 0.1210 | 9840 |
| mp-BRKGA | 0.9348 ± 0.0304 | 35.1733 ± 13.8560 | 39.7168 ± 19.9808 | 0.8674 ± 0.1146 | 9840 |
| single-pop BRKGA | 0.9151 ± 0.0469 | 24.1285 ± 25.7709 | 44.9690 ± 44.8674 | 0.8603 ± 0.0741 | 9840 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.084 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.989** |
| random baseline | 0.083 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 7.821. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

