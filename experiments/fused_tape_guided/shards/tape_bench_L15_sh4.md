# Faithful-guidance study -- L15 (N=16, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 80x4 = GAT/BRKGA 320/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9262 ± 0.0637 | 21.3001 ± 28.0528 | 20.4492 ± 23.6800 | 0.8599 ± 0.1644 | 13120 |
| E-HGATv2-attn | 0.8928 ± 0.0431 | 20.9489 ± 18.9678 | 19.4674 ± 14.0361 | 0.9202 ± 0.1608 | 13120 |
| NSGA-II (random) | 0.7678 ± 0.1121 | 54.5717 ± 34.1149 | 51.6527 ± 19.0470 | 0.7827 ± 0.1498 | 13120 |
| mp-BRKGA | 0.7753 ± 0.1308 | 91.2443 ± 87.2903 | 71.7802 ± 26.9489 | 0.7086 ± 0.2108 | 13120 |
| single-pop BRKGA | 0.7057 ± 0.1445 | 65.8096 ± 55.2857 | 52.4930 ± 28.2521 | 0.8546 ± 0.1828 | 13120 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | 0.064 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.996** |
| random baseline | 0.062 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 3.289. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

