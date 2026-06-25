# Critical-path worked examples (R2)

## toy:8 (N=8, AGV=2, QC=3, coupled=False, fused R2(Cmax)=0.997)

### makespan_optimal: C_max=316.667, E=10516.667 (GNN C_max=318.819); leg-Jaccard(GNN vs oracle)=1.000; decomposition consistent (sum on-path = 316.667)

| order | task | activity | duration (exact) | dC_max | GNN on-path | GNN duration | abs err |
|---|---|---|---|---|---|---|---|
| 0 | t2 | empty_leg | 50.000 | 1.00 | True | 47.996 | 2.004 |
| 1 | t2 | loaded_leg | 41.667 | 1.00 | True | 45.516 | 3.849 |
| 2 | t4 | empty_leg | 34.722 | 1.00 | True | 38.934 | 4.212 |
| 3 | t4 | loaded_leg | 83.333 | 1.00 | True | 80.063 | 3.270 |
| 4 | t5 | empty_leg | 6.944 | 1.00 | True | 8.292 | 1.347 |
| 5 | t5 | loaded_leg | 100.000 | 1.00 | True | 98.019 | 1.981 |

### energy_optimal: C_max=575.000, E=8612.500 (GNN C_max=568.414); leg-Jaccard(GNN vs oracle)=1.000; decomposition consistent (sum on-path = 575.000)

| order | task | activity | duration (exact) | dC_max | GNN on-path | GNN duration | abs err |
|---|---|---|---|---|---|---|---|
| 0 | t0 | empty_leg | 0.000 | 1.00 | True | 2.227 | 2.227 |
| 1 | t0 | loaded_leg | 62.500 | 1.00 | True | 59.257 | 3.243 |
| 2 | t5 | empty_leg | 20.833 | 1.00 | True | 21.024 | 0.190 |
| 3 | t5 | loaded_leg | 125.000 | 1.00 | True | 124.445 | 0.555 |
| 4 | t4 | empty_leg | 10.417 | 1.00 | True | 19.475 | 9.058 |
| 5 | t4 | loaded_leg | 125.000 | 1.00 | True | 113.294 | 11.706 |
| 6 | t4 | qc_handling | 45.000 | 1.00 | True | 47.203 | 2.203 |
| 7 | t7 | loaded_leg | 62.500 | 1.00 | True | 58.615 | 3.885 |
| 8 | t7 | qc_handling | 30.000 | 1.00 | True | 30.564 | 0.564 |
| 9 | t1 | empty_leg | 31.250 | 1.00 | True | 28.624 | 2.626 |
| 10 | t1 | loaded_leg | 62.500 | 1.00 | True | 63.687 | 1.187 |

