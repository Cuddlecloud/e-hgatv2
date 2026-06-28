# Faithful-guidance study -- L35 (N=12, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 60x4 = GAT/BRKGA 240/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9568 ± 0.0313 | 17.3661 ± 7.8132 | 23.0808 ± 2.6155 | 0.8446 ± 0.0978 | 9840 |
| E-HGATv2-attn | 0.9645 ± 0.0339 | 15.0685 ± 8.9784 | 18.0397 ± 11.5461 | 0.8571 ± 0.1576 | 9840 |
| NSGA-II (random) | 0.9372 ± 0.0271 | 21.5979 ± 17.5820 | 24.8581 ± 14.2479 | 0.8769 ± 0.1499 | 9840 |
| mp-BRKGA | 0.9200 ± 0.0656 | 38.7893 ± 32.7875 | 48.6850 ± 50.5778 | 0.8863 ± 0.1668 | 9840 |
| single-pop BRKGA | 0.9124 ± 0.0136 | 33.7112 ± 26.5436 | 39.4134 ± 11.6726 | 0.8224 ± 0.1502 | 9840 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.600 | 0.084 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.989** |
| random baseline | 0.083 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 7.821. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

