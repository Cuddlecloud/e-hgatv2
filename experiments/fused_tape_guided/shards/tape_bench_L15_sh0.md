# Faithful-guidance study -- L15 (N=16, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 80x4 = GAT/BRKGA 320/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.8977 ± 0.1373 | 36.6693 ± 55.2326 | 26.4545 ± 30.2623 | 0.8983 ± 0.1271 | 13120 |
| E-HGATv2-attn | 0.8999 ± 0.0293 | 20.9071 ± 15.1893 | 18.8855 ± 11.7157 | 0.9051 ± 0.1041 | 13120 |
| NSGA-II (random) | 0.8006 ± 0.0676 | 50.8335 ± 37.1071 | 40.5563 ± 12.2482 | 0.7902 ± 0.0337 | 13120 |
| mp-BRKGA | 0.7645 ± 0.0431 | 100.7782 ± 72.1497 | 57.2102 ± 6.5375 | 0.8136 ± 0.0959 | 13120 |
| single-pop BRKGA | 0.8201 ± 0.0906 | 33.3642 ± 18.2749 | 36.1316 ± 18.3830 | 0.8346 ± 0.1768 | 13120 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | 0.064 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.996** |
| random baseline | 0.062 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 3.289. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

