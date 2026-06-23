# mp-BRKGA vs E-HGATv2 vs single-pop BRKGA -- toy:10 (N=10)

_5 seeds, 60 gens, matched true-eval budget (mp 200x4 = single/GAT 800 per gen). Reference: non-dominated union of 3 methods @ 150 gens. Cells = mean (95% CI)._

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-NSGA-II | 0.9879 ± 0.0087 | 7.3219 ± 7.6411 | 6.8626 ± 6.6772 | 0.7645 ± 0.0724 | 48800 |
| mp-BRKGA | 0.9021 ± 0.0887 | 133.7439 ± 156.8748 | 42.0156 ± 40.8843 | 0.9143 ± 0.0709 | 48800 |
| single-pop BRKGA | 0.9034 ± 0.0432 | 23.6361 ± 25.6298 | 54.0188 ± 28.0579 | 0.9480 ± 0.0960 | 48800 |
