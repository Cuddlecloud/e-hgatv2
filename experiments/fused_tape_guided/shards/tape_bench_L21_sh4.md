# Faithful-guidance study -- L21 (N=12, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 60x4 = GAT/BRKGA 240/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9383 ± 0.0253 | 6.7349 ± 5.3866 | 8.6668 ± 4.9743 | 0.7202 ± 0.1686 | 9840 |
| E-HGATv2-attn | 0.9043 ± 0.0800 | 5.6736 ± 5.6042 | 8.7248 ± 5.3736 | 0.8821 ± 0.0732 | 9840 |
| NSGA-II (random) | 0.8416 ± 0.0655 | 19.0983 ± 17.8004 | 17.8740 ± 7.8229 | 0.8617 ± 0.0651 | 9840 |
| mp-BRKGA | 0.7077 ± 0.2175 | 92.4659 ± 88.2482 | 40.4329 ± 30.8460 | 0.8985 ± 0.1968 | 9840 |
| single-pop BRKGA | 0.8470 ± 0.1025 | 27.7169 ± 54.4549 | 21.8557 ± 21.9444 | 0.9531 ± 0.2131 | 9840 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.733 | 0.054 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.988** |
| random baseline | 0.083 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 2.184. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

