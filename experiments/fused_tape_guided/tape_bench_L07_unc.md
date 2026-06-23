# Faithful-guidance study -- L07 (N=8, uncoupled)

_5 seeds, 40 gens, matched exact-eval budget (mp 40x4 = GAT/BRKGA 160/gen). Reference: non-dominated union of mp-BRKGA + BRKGA + TAPE @ 50 gens. Cells = mean (95% CI)._

## Optimisation (Req 3)

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-TAPE | 0.9725 ± 0.0100 | 10.5437 ± 6.7295 | 17.2127 ± 10.6162 | 0.8255 ± 0.0626 | 6560 |
| E-HGATv2-attn | 0.9783 ± 0.0202 | 2.0269 ± 0.9556 | 12.3271 ± 15.3816 | 0.8374 ± 0.1185 | 6560 |
| NSGA-II (random) | 0.9651 ± 0.0086 | 8.0661 ± 11.8354 | 17.2132 ± 6.4781 | 0.8692 ± 0.1482 | 6560 |
| mp-BRKGA | 0.8952 ± 0.0560 | 56.9704 ± 39.9560 | 40.2150 ± 17.3665 | 0.8363 ± 0.1039 | 6560 |
| single-pop BRKGA | 0.9496 ± 0.0396 | 10.5221 ± 3.9377 | 20.0790 ± 20.4465 | 0.8389 ± 0.0554 | 6560 |

## Guidance-signal faithfulness (Req 2)

| Signal | precision@1 | Spearman rho | leg-critical Jaccard vs oracle |
|---|---|---|---|
| attention (Signal #1) | 0.867 | 0.171 | n/a |
| **TAPE (Signal #3)** | n/a | n/a | **0.985** |
| random baseline | 0.125 | 0.000 | n/a |

_TAPE makespan abs-error vs oracle: 2.220. A faithful signal that also tops the optimisation table is the unified Req 2+3 claim._

