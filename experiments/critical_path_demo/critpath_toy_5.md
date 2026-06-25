# Critical-path worked examples (R2)

## toy:5 (N=5, AGV=2, QC=3, coupled=False, fused R2(Cmax)=0.998)

### makespan_optimal: C_max=232.500, E=7166.667 (GNN C_max=236.337); leg-Jaccard(GNN vs oracle)=1.000; decomposition consistent (sum on-path = 232.500)

| order | task | activity | duration (exact) | dC_max | GNN on-path | GNN duration | abs err |
|---|---|---|---|---|---|---|---|
| 0 | t3 | empty_leg | 20.833 | 1.00 | True | 23.351 | 2.518 |
| 1 | t3 | loaded_leg | 83.333 | 1.00 | True | 80.659 | 2.674 |
| 2 | t2 | empty_leg | 6.944 | 1.00 | True | 7.640 | 0.696 |
| 3 | t2 | loaded_leg | 41.667 | 1.00 | True | 41.919 | 0.253 |
| 4 | t1 | empty_leg | 34.722 | 1.00 | True | 38.578 | 3.855 |
| 5 | t4 | qc_handling | 45.000 | 1.00 | True | 44.189 | 0.811 |

### energy_optimal: C_max=723.000, E=5606.250 (GNN C_max=706.194); leg-Jaccard(GNN vs oracle)=1.000; decomposition consistent (sum on-path = 723.000)

| order | task | activity | duration (exact) | dC_max | GNN on-path | GNN duration | abs err |
|---|---|---|---|---|---|---|---|
| 0 | t0 | empty_leg | 0.000 | 1.00 | True | 0.876 | 0.876 |
| 1 | t0 | loaded_leg | 62.500 | 1.00 | True | 59.672 | 2.828 |
| 2 | t0 | qc_handling | 73.000 | 1.00 | True | 72.999 | 0.001 |
| 3 | t3 | loaded_leg | 125.000 | 1.00 | True | 121.192 | 3.808 |
| 4 | t3 | qc_handling | 43.000 | 1.00 | True | 42.979 | 0.021 |
| 5 | t2 | empty_leg | 10.417 | 1.00 | True | 12.574 | 2.158 |
| 6 | t2 | loaded_leg | 62.500 | 1.00 | True | 58.672 | 3.828 |
| 7 | t4 | empty_leg | 52.083 | 1.00 | True | 52.694 | 0.610 |
| 8 | t4 | loaded_leg | 125.000 | 1.00 | True | 121.255 | 3.745 |
| 9 | t4 | qc_handling | 45.000 | 1.00 | True | 45.642 | 0.642 |
| 10 | t1 | loaded_leg | 62.500 | 1.00 | True | 56.080 | 6.420 |
| 11 | t1 | qc_handling | 62.000 | 1.00 | True | 61.559 | 0.441 |

