# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 400x4 = GAT/BRKGA 1600/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.4647 ± 0.0000 | 925.6761 ± 0.0000 | 1715.2514 ± 0.0000 | 0.8849 ± 0.0000 | 65600 |
| E-HGATv2-attn | 0.6180 ± 0.0000 | 965.9092 ± 0.0000 | 984.8212 ± 0.0000 | 0.9571 ± 0.0000 | 65600 |
| NSGA-II (random) | 0.1090 ± 0.0000 | 3051.2384 ± 0.0000 | 3938.4404 ± 0.0000 | 0.9811 ± 0.0000 | 65600 |
| mp-BRKGA | 0.3847 ± 0.0000 | 2346.4299 ± 0.0000 | 1403.9179 ± 0.0000 | 0.9303 ± 0.0000 | 65600 |
| single-pop BRKGA | 0.0520 ± 0.0000 | 3988.0696 ± 0.0000 | 4628.7736 ± 0.0000 | 0.9164 ± 0.0000 | 65600 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

