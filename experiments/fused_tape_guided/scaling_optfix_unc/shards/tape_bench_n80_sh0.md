# Faithful-guidance study -- toy:80 (N=80, uncoupled)

_1 seeds, 40 gens, matched exact-eval budget (mp 100x4 = GAT/BRKGA 400/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8364 ± 0.0000 | 353.1622 ± 0.0000 | 1155.6480 ± 0.0000 | 0.9154 ± 0.0000 | 16400 |
| E-HGATv2-attn | 0.7836 ± 0.0000 | 323.1430 ± 0.0000 | 1436.2011 ± 0.0000 | 0.9214 ± 0.0000 | 16400 |
| NSGA-II (random) | 0.6374 ± 0.0000 | 873.1669 ± 0.0000 | 2354.3766 ± 0.0000 | 0.8799 ± 0.0000 | 16400 |
| mp-BRKGA | 0.9126 ± 0.0000 | 229.9321 ± 0.0000 | 259.1451 ± 0.0000 | 0.8240 ± 0.0000 | 16400 |
| single-pop BRKGA | 0.7272 ± 0.0000 | 402.0715 ± 0.0000 | 1265.7821 ± 0.0000 | 0.7775 ± 0.0000 | 16400 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.567 | -0.020 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.974** |
| random baseline | 0.013 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 40.417. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

