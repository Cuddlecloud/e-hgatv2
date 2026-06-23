# mp-BRKGA vs E-HGATv2 vs single-pop BRKGA -- toy:5 (N=5)

_3 seeds, 40 gens, matched true-eval budget (mp 100x4 = single/GAT 400 per gen). Reference: exact Oracle. Cells = mean (95% CI)._

| Method | HV / HV* | GD+ | IGD+ | Spread | true evals |
|---|---|---|---|---|---|
| E-HGATv2-NSGA-II | 0.9893 ± 0.0001 | 0.9789 ± 0.0769 | 2.5693 ± 0.0621 | 0.9549 ± 0.0132 | 16400 |
| mp-BRKGA | 0.9945 ± 0.0051 | 1.5683 ± 1.2300 | 2.4974 ± 1.8089 | 0.8931 ± 0.1726 | 16400 |
| single-pop BRKGA | 0.9956 ± 0.0082 | 0.7344 ± 0.2267 | 1.4582 ± 1.4637 | 0.8899 ± 0.1024 | 16400 |
