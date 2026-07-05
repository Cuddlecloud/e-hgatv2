# Faithful-guidance study -- toy:10 (N=10, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 50x4 = GAT/BRKGA 200/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9666 ± 0.0000 | 16.4470 ± 0.0000 | 16.4441 ± 0.0000 | 0.8999 ± 0.0000 | 8200 |
| E-HGATv2-attn | 0.9437 ± 0.0000 | 41.2019 ± 0.0000 | 25.6251 ± 0.0000 | 0.9845 ± 0.0000 | 8200 |
| NSGA-II (random) | 0.8578 ± 0.0000 | 109.6315 ± 0.0000 | 69.1316 ± 0.0000 | 0.9781 ± 0.0000 | 8200 |
| mp-BRKGA | 0.7993 ± 0.0000 | 91.5726 ± 0.0000 | 131.3930 ± 0.0000 | 0.8630 ± 0.0000 | 8200 |
| single-pop BRKGA | 0.9283 ± 0.0000 | 4.2888 ± 0.0000 | 26.4639 ± 0.0000 | 0.8255 ± 0.0000 | 8200 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.700 | 0.088 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.100 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 10.516. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

