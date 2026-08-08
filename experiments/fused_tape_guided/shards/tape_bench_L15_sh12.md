# Faithful-guidance study -- L15 (N=16, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 80x4 = GAT/BRKGA 320/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9445 ± 0.0265 | 23.8667 ± 9.6030 | 26.6848 ± 3.9557 | 0.8540 ± 0.0209 | 13120 |
| E-HGATv2-attn | 0.9332 ± 0.0265 | 18.7795 ± 18.2583 | 22.1304 ± 17.8707 | 0.8742 ± 0.1855 | 13120 |
| NSGA-II (random) | 0.8853 ± 0.0304 | 42.4831 ± 24.2954 | 43.3591 ± 18.6875 | 0.8254 ± 0.0548 | 13120 |
| mp-BRKGA | 0.8447 ± 0.0630 | 69.3486 ± 13.2539 | 75.8307 ± 9.6661 | 0.7743 ± 0.0378 | 13120 |
| single-pop BRKGA | 0.8598 ± 0.0560 | 48.1067 ± 42.9341 | 52.9100 ± 44.1420 | 0.8721 ± 0.2006 | 13120 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | 0.064 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.996** |
| random baseline | 0.062 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 3.289. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

