# Pareto-front behaviour via TAPE PTS (coupled)

_Per instance: lambda sweep across the front, the top bottleneck tasks at the makespan-optimal vs energy-optimal extreme, the bottleneck migration (1 - Jaccard of top-3 at the two extremes), and the PTS concentration (share of total tension on the top-3 tasks)._

| Instance | N | front | lambda range | top-3 (Cmax end) | top-3 (E end) | migration | PTS conc.@3 |
|---|---|---|---|---|---|---|---|
| toy:10 | 10 | 54 | [0.00, 1.00] | [0, 1, 3] | [0, 1, 2] | 0.50 | 0.51 |
| toy:20 | 20 | 24 | [0.76, 1.00] | [0, 2, 7] | [0, 1, 3] | 0.80 | 0.31 |
