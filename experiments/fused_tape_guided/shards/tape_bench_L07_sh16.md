# Faithful-guidance study -- L07 (N=8, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 40x4 = GAT/BRKGA 160/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9809 ± 0.0396 | 7.3214 ± 18.0518 | 13.1526 ± 32.2264 | 0.8223 ± 0.2619 | 6560 |
| E-HGATv2-attn | 0.9928 ± 0.0110 | 2.1967 ± 2.5777 | 3.8097 ± 2.2274 | 0.8017 ± 0.0757 | 6560 |
| NSGA-II (random) | 0.9484 ± 0.0263 | 6.0781 ± 5.6148 | 35.0103 ± 26.0598 | 0.8094 ± 0.0917 | 6560 |
| mp-BRKGA | 0.9314 ± 0.0393 | 31.7839 ± 23.2403 | 33.3693 ± 28.5161 | 0.7866 ± 0.2488 | 6560 |
| single-pop BRKGA | 0.9329 ± 0.0143 | 6.0745 ± 9.4266 | 37.9336 ± 18.2748 | 0.8477 ± 0.0164 | 6560 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.867 | 0.176 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.985** |
| random baseline | 0.125 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 2.221. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

