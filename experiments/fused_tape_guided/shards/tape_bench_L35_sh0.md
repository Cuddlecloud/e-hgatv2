# Faithful-guidance study -- L35 (N=12, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 60x4 = GAT/BRKGA 240/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9476 ± 0.0152 | 16.5748 ± 15.6575 | 21.4654 ± 14.0640 | 0.8445 ± 0.0958 | 9840 |
| E-HGATv2-attn | 0.9440 ± 0.0151 | 13.7805 ± 6.7507 | 16.9529 ± 5.4138 | 0.9347 ± 0.1443 | 9840 |
| NSGA-II (random) | 0.9102 ± 0.0391 | 29.7441 ± 19.3177 | 30.3566 ± 11.8754 | 0.9465 ± 0.1137 | 9840 |
| mp-BRKGA | 0.8985 ± 0.0573 | 44.8618 ± 22.5729 | 58.8023 ± 41.0472 | 0.8912 ± 0.1616 | 9840 |
| single-pop BRKGA | 0.8942 ± 0.0323 | 34.0255 ± 21.5744 | 45.8590 ± 25.5073 | 0.9109 ± 0.1166 | 9840 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.084 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.989** |
| random baseline | 0.083 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 7.821. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

