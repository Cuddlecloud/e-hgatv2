# Pareto-front behaviour via TAPE TCS (uncoupled)

_Per instance: lambda sweep across the front, the top bottleneck tasks at the makespan-optimal vs energy-optimal extreme, the bottleneck migration (1 - Jaccard of top-3 at the two extremes), and the TCS concentration (share of total criticality on the top-3 tasks)._

| Instance | N | front | lambda range | top-3 (Cmax end) | top-3 (E end) | migration | TCS conc.@3 |
|---|---|---|---|---|---|---|---|
| toy:5 | 5 | 84 | [0.20, 1.00] | [1, 2, 3] | [0, 2, 4] | 0.80 | 0.84 |
| toy:8 | 8 | 116 | [0.00, 1.00] | [2, 3, 5] | [2, 3, 4] | 0.50 | 0.67 |
| toy:10 | 10 | 47 | [0.17, 1.00] | [1, 2, 3] | [0, 2, 4] | 0.80 | 0.56 |
| toy:15 | 15 | 29 | [0.30, 0.96] | [1, 2, 3] | [2, 6, 7] | 0.80 | 0.34 |
| toy:20 | 20 | 28 | [0.56, 1.00] | [3, 4, 5] | [0, 6, 7] | 1.00 | 0.30 |
| L07 | 8 | 49 | [0.08, 0.99] | [1, 5, 6] | [1, 4, 6] | 0.50 | 0.71 |
| L15 | 16 | 33 | [0.39, 1.00] | [0, 2, 4] | [4, 5, 6] | 0.80 | 0.33 |
| L21 | 12 | 37 | [0.45, 1.00] | [5, 10, 0] | [5, 8, 9] | 0.80 | 0.59 |
| L35 | 12 | 48 | [0.00, 1.00] | [2, 3, 5] | [0, 1, 6] | 1.00 | 0.45 |
