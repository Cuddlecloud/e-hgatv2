# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_5 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9484 ± 0.0864 | 27.9918 ± 26.9661 | 52.5363 ± 65.8522 | 0.9392 ± 0.1737 | 8200 |
| E-HGATv2-attn | 1.0025 ± 0.0325 | 8.6898 ± 14.1536 | 17.0273 ± 14.1875 | 0.9093 ± 0.0897 | 8200 |
| NSGA-II (random) | 0.9251 ± 0.0723 | 42.8153 ± 39.6630 | 46.2794 ± 33.2963 | 0.9005 ± 0.0712 | 8200 |
| mp-BRKGA | 0.8859 ± 0.0758 | 79.7377 ± 55.1723 | 73.6680 ± 33.8690 | 0.8268 ± 0.0973 | 8200 |
| single-pop BRKGA | 0.9533 ± 0.0309 | 30.3851 ± 12.9416 | 31.3886 ± 13.7852 | 0.8987 ± 0.0324 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 11.113. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

