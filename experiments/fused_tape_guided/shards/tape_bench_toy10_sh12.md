# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8838 ± 0.0364 | 100.8314 ± 116.9484 | 44.5980 ± 22.8503 | 1.0173 ± 0.1634 | 8200 |
| E-HGATv2-attn | 0.8767 ± 0.1131 | 80.9058 ± 74.0616 | 54.6085 ± 53.7664 | 0.9091 ± 0.1028 | 8200 |
| NSGA-II (random) | 0.8642 ± 0.0751 | 82.0600 ± 141.5073 | 53.8230 ± 34.9838 | 0.9063 ± 0.1790 | 8200 |
| mp-BRKGA | 0.7446 ± 0.1339 | 277.2081 ± 228.5846 | 126.8147 ± 77.6246 | 0.8970 ± 0.1725 | 8200 |
| single-pop BRKGA | 0.7918 ± 0.1268 | 79.5496 ± 92.7751 | 96.5133 ± 87.6006 | 0.9043 ± 0.2353 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

