# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9819 ± 0.0000 | 6.6472 ± 0.0000 | 11.0629 ± 0.0000 | 0.7851 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9719 ± 0.0000 | 10.9455 ± 0.0000 | 12.9115 ± 0.0000 | 0.9893 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.8255 ± 0.0000 | 197.7949 ± 0.0000 | 79.3212 ± 0.0000 | 0.9625 ± 0.0000 | 8200 |
| mp-BRKGA | 0.6657 ± 0.0000 | 161.8443 ± 0.0000 | 179.4570 ± 0.0000 | 0.7704 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.9086 ± 0.0000 | 19.2429 ± 0.0000 | 33.2660 ± 0.0000 | 0.9118 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

