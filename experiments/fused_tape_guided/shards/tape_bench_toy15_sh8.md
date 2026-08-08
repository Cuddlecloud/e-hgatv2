# Faithful-guidance study -- toy:15 (N=15, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 75x4 = GAT/BRKGA 300/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8401 ± 0.0514 | 91.3984 ± 22.3865 | 125.1509 ± 70.6703 | 0.8988 ± 0.1356 | 12300 |
| E-HGATv2-attn | 0.8964 ± 0.0572 | 49.1783 ± 28.6698 | 85.4605 ± 70.9860 | 0.8803 ± 0.0680 | 12300 |
| NSGA-II (random) | 0.7723 ± 0.0811 | 152.3186 ± 102.0755 | 209.3087 ± 154.9741 | 0.8748 ± 0.1232 | 12300 |
| mp-BRKGA | 0.8041 ± 0.0328 | 123.1078 ± 69.7775 | 127.0434 ± 32.2507 | 0.8816 ± 0.0947 | 12300 |
| single-pop BRKGA | 0.8246 ± 0.0375 | 83.6008 ± 71.7370 | 135.9712 ± 61.2860 | 0.8844 ± 0.2250 | 12300 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.800 | 0.081 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.975** |
| random baseline | 0.067 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 14.749. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

