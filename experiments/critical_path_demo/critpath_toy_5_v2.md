# Critical-path worked examples (R2)

## toy:5 (N=5, AGV=2, QC=3, coupled=False, fused R2(Cmax)=0.999)

### makespan_optimal: C_max=232.500, E=7166.667 (GNN C_max=235.996); leg-Jaccard(GNN vs oracle)=1.000; decomposition consistent (sum on-path = 232.500)

| order | task | activity | duration (exact) | dC_max | GNN on-path | GNN duration | abs err |
|---|---|---|---|---|---|---|---|
| 0 | t3 | empty_leg | 20.833 | 1.00 | True | 23.714 | 2.881 |
| 1 | t3 | loaded_leg | 83.333 | 1.00 | True | 80.076 | 3.258 |
| 2 | t2 | empty_leg | 6.944 | 1.00 | True | 7.115 | 0.170 |
| 3 | t2 | loaded_leg | 41.667 | 1.00 | True | 42.128 | 0.461 |
| 4 | t1 | empty_leg | 34.722 | 1.00 | True | 38.307 | 3.585 |
| 5 | t4 | qc_handling | 45.000 | 1.00 | True | 44.657 | 0.343 |

### energy_optimal: C_max=723.000, E=5606.250 (GNN C_max=707.498); leg-Jaccard(GNN vs oracle)=1.000; decomposition consistent (sum on-path = 723.000)

| order | task | activity | duration (exact) | dC_max | GNN on-path | GNN duration | abs err |
|---|---|---|---|---|---|---|---|
| 0 | t0 | empty_leg | 0.000 | 1.00 | True | 1.042 | 1.042 |
| 1 | t0 | loaded_leg | 62.500 | 1.00 | True | 60.040 | 2.460 |
| 2 | t0 | qc_handling | 73.000 | 1.00 | True | 72.989 | 0.011 |
| 3 | t3 | loaded_leg | 125.000 | 1.00 | True | 120.918 | 4.082 |
| 4 | t3 | qc_handling | 43.000 | 1.00 | True | 42.982 | 0.018 |
| 5 | t2 | empty_leg | 10.417 | 1.00 | True | 13.459 | 3.042 |
| 6 | t2 | loaded_leg | 62.500 | 1.00 | True | 58.681 | 3.819 |
| 7 | t4 | empty_leg | 52.083 | 1.00 | True | 53.353 | 1.269 |
| 8 | t4 | loaded_leg | 125.000 | 1.00 | True | 121.066 | 3.934 |
| 9 | t4 | qc_handling | 45.000 | 1.00 | True | 45.433 | 0.433 |
| 10 | t1 | loaded_leg | 62.500 | 1.00 | True | 56.025 | 6.475 |
| 11 | t1 | qc_handling | 62.000 | 1.00 | True | 61.513 | 0.487 |

