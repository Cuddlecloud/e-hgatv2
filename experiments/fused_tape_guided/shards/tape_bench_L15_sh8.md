# Faithful-guidance study -- L15 (N=16, uncoupled)

_4 seeds, 40 gens, matched exact-eval budget (mp 80x4 = GAT/BRKGA 320/gen). Reference: non-dominated union of high-budget mp-BRKGA + BRKGA + TAPE @ 50 gens and all evaluated fronts. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9659 ± 0.0313 | 18.1239 ± 29.3956 | 19.5195 ± 26.5773 | 0.8407 ± 0.0500 | 13120 |
| E-HGATv2-attn | 0.9558 ± 0.0174 | 19.4299 ± 19.8403 | 22.3679 ± 17.6801 | 0.8710 ± 0.1047 | 13120 |
| NSGA-II (random) | 0.9033 ± 0.0168 | 52.9248 ± 18.9081 | 54.2086 ± 13.6425 | 0.8349 ± 0.0664 | 13120 |
| mp-BRKGA | 0.9246 ± 0.0342 | 55.8036 ± 22.7524 | 63.8350 ± 16.6490 | 0.7215 ± 0.0838 | 13120 |
| single-pop BRKGA | 0.9069 ± 0.0523 | 35.9456 ± 33.4924 | 45.8756 ± 34.2529 | 0.8802 ± 0.0609 | 13120 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.667 | 0.064 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.996** |
| random baseline | 0.062 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 3.289. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

