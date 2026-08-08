# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9240 ± 0.0832 | 29.7947 ± 35.0048 | 57.0529 ± 76.8174 | 0.9237 ± 0.0845 | 8200 |
| E-HGATv2-attn | 0.9069 ± 0.0204 | 29.3526 ± 22.1190 | 82.7965 ± 29.5667 | 0.9399 ± 0.1221 | 8200 |
| NSGA-II (random) | 0.8206 ± 0.0706 | 83.4478 ± 66.6984 | 130.1891 ± 40.5655 | 0.9080 ± 0.0983 | 8200 |
| mp-BRKGA | 0.7849 ± 0.0940 | 127.6342 ± 93.5676 | 135.6579 ± 87.5978 | 0.8374 ± 0.1377 | 8200 |
| single-pop BRKGA | 0.8683 ± 0.0458 | 56.5914 ± 42.5343 | 77.7719 ± 35.1311 | 0.8926 ± 0.0321 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

