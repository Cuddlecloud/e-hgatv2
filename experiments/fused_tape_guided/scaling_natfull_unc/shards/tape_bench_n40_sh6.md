# Faithful-guidance study -- toy:40 (N=40, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 200x4 = GAT/BRKGA 800/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 15 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9267 ± 0.0000 | 0.0000 ± 0.0000 | 264.5363 ± 0.0000 | 0.9966 ± 0.0000 | 32800 |
| E-HGATv2-attn | 0.8010 ± 0.0000 | 292.3511 ± 0.0000 | 654.0908 ± 0.0000 | 0.9213 ± 0.0000 | 32800 |
| NSGA-II (random) | 0.6776 ± 0.0000 | 261.8423 ± 0.0000 | 1286.0411 ± 0.0000 | 0.7935 ± 0.0000 | 32800 |
| mp-BRKGA | 0.8943 ± 0.0000 | 113.2409 ± 0.0000 | 274.5131 ± 0.0000 | 0.8243 ± 0.0000 | 32800 |
| single-pop BRKGA | 0.6298 ± 0.0000 | 508.4406 ± 0.0000 | 1553.9450 ± 0.0000 | 0.9166 ± 0.0000 | 32800 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | -0.065 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.978** |
| random baseline | 0.025 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 26.691. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

