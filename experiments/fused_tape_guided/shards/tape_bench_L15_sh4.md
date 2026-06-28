# Faithful-guidance study -- L15 (N=16, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 80x4 = GAT/BRKGA 320/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8746 ± 0.0405 | 29.6543 ± 9.7940 | 24.5473 ± 5.5254 | 0.9242 ± 0.2499 | 13120 |
| E-HGATv2-attn | 0.8770 ± 0.1256 | 21.6003 ± 21.6668 | 22.1749 ± 23.4142 | 0.9518 ± 0.0641 | 13120 |
| NSGA-II (random) | 0.7982 ± 0.1175 | 38.8665 ± 9.7372 | 37.0871 ± 14.1643 | 0.8995 ± 0.1572 | 13120 |
| mp-BRKGA | 0.8144 ± 0.0638 | 75.0661 ± 42.6439 | 54.3607 ± 19.2616 | 0.7409 ± 0.0956 | 13120 |
| single-pop BRKGA | 0.7181 ± 0.0965 | 54.5931 ± 21.2427 | 54.8995 ± 20.2567 | 0.9719 ± 0.1782 | 13120 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | 0.064 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.996** |
| random baseline | 0.062 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 3.289. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

