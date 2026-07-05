# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8520 ± 0.0000 | 123.5365 ± 0.0000 | 394.1649 ± 0.0000 | 0.9797 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.8338 ± 0.0000 | 255.0363 ± 0.0000 | 400.4936 ± 0.0000 | 0.8074 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.5631 ± 0.0000 | 421.0325 ± 0.0000 | 1488.6051 ± 0.0000 | 0.7830 ± 0.0000 | 32800 |
| mp-BRKGA | 0.7636 ± 0.0000 | 565.4594 ± 0.0000 | 559.4470 ± 0.0000 | 0.7974 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.5885 ± 0.0000 | 856.6328 ± 0.0000 | 1197.4829 ± 0.0000 | 0.7456 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

