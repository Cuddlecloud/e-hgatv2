# Critical-path worked examples (R2)

## toy:10 (N=10, AGV=2, QC=3, coupled=False, fused R2(Cmax)=0.998)

### makespan_optimal: C_max=454.167, E=14316.667 (GNN C_max=454.772); leg-Jaccard(GNN vs oracle)=1.000; decomposition consistent (sum on-path = 454.167)

| order | task | activity | duration (exact) | dC_max | GNN on-path | GNN duration | abs err |
|---|---|---|---|---|---|---|---|
| 0 | t0 | empty_leg | 0.000 | 1.00 | True | 0.000 | 0.000 |
| 1 | t0 | loaded_leg | 41.667 | 1.00 | True | 43.975 | 2.308 |
| 2 | t5 | empty_leg | 13.889 | 1.00 | True | 13.566 | 0.323 |
| 3 | t5 | loaded_leg | 83.333 | 1.00 | True | 83.114 | 0.219 |
| 4 | t4 | empty_leg | 8.333 | 1.00 | True | 9.703 | 1.370 |
| 5 | t4 | loaded_leg | 83.333 | 1.00 | True | 81.826 | 1.507 |
| 6 | t8 | empty_leg | 27.778 | 1.00 | True | 29.674 | 1.896 |
| 7 | t8 | loaded_leg | 41.667 | 1.00 | True | 36.453 | 5.214 |
| 8 | t1 | empty_leg | 41.667 | 1.00 | True | 40.627 | 1.040 |
| 9 | t1 | loaded_leg | 50.000 | 1.00 | True | 52.055 | 2.055 |
| 10 | t7 | empty_leg | 20.833 | 1.00 | True | 23.478 | 2.645 |
| 11 | t7 | loaded_leg | 41.667 | 1.00 | True | 40.301 | 1.366 |

### energy_optimal: C_max=925.583, E=10743.750 (GNN C_max=922.437); leg-Jaccard(GNN vs oracle)=1.000; decomposition consistent (sum on-path = 925.583)

| order | task | activity | duration (exact) | dC_max | GNN on-path | GNN duration | abs err |
|---|---|---|---|---|---|---|---|
| 0 | t0 | empty_leg | 0.000 | 1.00 | True | 1.413 | 1.413 |
| 1 | t0 | loaded_leg | 62.500 | 1.00 | True | 60.565 | 1.935 |
| 2 | t0 | qc_handling | 73.000 | 1.00 | True | 72.984 | 0.016 |
| 3 | t3 | loaded_leg | 125.000 | 1.00 | True | 124.946 | 0.054 |
| 4 | t3 | qc_handling | 43.000 | 1.00 | True | 42.505 | 0.495 |
| 5 | t8 | empty_leg | 10.417 | 1.00 | True | 12.647 | 2.230 |
| 6 | t8 | loaded_leg | 62.500 | 1.00 | True | 58.876 | 3.624 |
| 7 | t8 | qc_handling | 38.000 | 1.00 | True | 38.473 | 0.473 |
| 8 | t5 | loaded_leg | 125.000 | 1.00 | True | 123.644 | 1.356 |
| 9 | t5 | qc_handling | 32.000 | 1.00 | True | 31.799 | 0.201 |
| 10 | t4 | empty_leg | 10.417 | 1.00 | True | 16.620 | 6.203 |
| 11 | t4 | loaded_leg | 125.000 | 1.00 | True | 119.539 | 5.461 |
| 12 | t4 | qc_handling | 45.000 | 1.00 | True | 45.000 | 0.000 |
| 13 | t7 | loaded_leg | 50.000 | 1.00 | True | 50.542 | 0.542 |
| 14 | t7 | qc_handling | 30.000 | 1.00 | True | 29.400 | 0.600 |
| 15 | t1 | empty_leg | 31.250 | 1.00 | True | 31.214 | 0.036 |
| 16 | t1 | loaded_leg | 62.500 | 1.00 | True | 62.270 | 0.230 |

