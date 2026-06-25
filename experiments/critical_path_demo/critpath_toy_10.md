# Critical-path worked examples (R2)

## toy:10 (N=10, AGV=2, QC=3, coupled=False, fused R2(Cmax)=0.997)

### makespan_optimal: C_max=436.611, E=12895.833 (GNN C_max=435.340); leg-Jaccard(GNN vs oracle)=1.000; decomposition consistent (sum on-path = 436.611)

| order | task | activity | duration (exact) | dC_max | GNN on-path | GNN duration | abs err |
|---|---|---|---|---|---|---|---|
| 0 | t1 | empty_leg | 27.778 | 1.00 | True | 30.670 | 2.892 |
| 1 | t1 | loaded_leg | 41.667 | 1.00 | True | 39.479 | 2.187 |
| 2 | t6 | empty_leg | 8.333 | 1.00 | True | 8.654 | 0.321 |
| 3 | t6 | loaded_leg | 50.000 | 1.00 | True | 49.464 | 0.536 |
| 4 | t7 | empty_leg | 6.944 | 1.00 | True | 9.876 | 2.932 |
| 5 | t7 | loaded_leg | 41.667 | 1.00 | True | 38.858 | 2.808 |
| 6 | t3 | empty_leg | 27.778 | 1.00 | True | 30.743 | 2.965 |
| 7 | t3 | loaded_leg | 83.333 | 1.00 | True | 79.211 | 4.122 |
| 8 | t2 | empty_leg | 6.944 | 1.00 | True | 10.807 | 3.863 |
| 9 | t2 | loaded_leg | 41.667 | 1.00 | True | 37.113 | 4.554 |
| 10 | t8 | empty_leg | 20.833 | 1.00 | True | 22.689 | 1.856 |
| 11 | t8 | loaded_leg | 41.667 | 1.00 | True | 39.169 | 2.498 |
| 12 | t8 | qc_handling | 38.000 | 1.00 | True | 38.605 | 0.605 |

### energy_optimal: C_max=908.750, E=10937.500 (GNN C_max=902.548); leg-Jaccard(GNN vs oracle)=1.000; decomposition consistent (sum on-path = 908.750)

| order | task | activity | duration (exact) | dC_max | GNN on-path | GNN duration | abs err |
|---|---|---|---|---|---|---|---|
| 0 | t0 | empty_leg | 0.000 | 1.00 | True | 2.104 | 2.104 |
| 1 | t0 | loaded_leg | 62.500 | 1.00 | True | 59.547 | 2.953 |
| 2 | t0 | qc_handling | 73.000 | 1.00 | True | 72.943 | 0.057 |
| 3 | t6 | qc_handling | 33.000 | 1.00 | True | 33.019 | 0.019 |
| 4 | t9 | loaded_leg | 125.000 | 1.00 | True | 125.358 | 0.358 |
| 5 | t9 | qc_handling | 71.000 | 1.00 | True | 70.495 | 0.505 |
| 6 | t2 | empty_leg | 8.333 | 1.00 | True | 13.178 | 4.845 |
| 7 | t2 | loaded_leg | 62.500 | 1.00 | True | 57.438 | 5.062 |
| 8 | t2 | qc_handling | 56.000 | 1.00 | True | 54.780 | 1.220 |
| 9 | t5 | loaded_leg | 125.000 | 1.00 | True | 120.591 | 4.409 |
| 10 | t5 | qc_handling | 32.000 | 1.00 | True | 31.856 | 0.144 |
| 11 | t4 | empty_leg | 10.417 | 1.00 | True | 17.639 | 7.222 |
| 12 | t4 | loaded_leg | 125.000 | 1.00 | True | 119.384 | 5.616 |
| 13 | t4 | qc_handling | 45.000 | 1.00 | True | 44.653 | 0.347 |
| 14 | t7 | loaded_leg | 50.000 | 1.00 | True | 49.927 | 0.073 |
| 15 | t7 | qc_handling | 30.000 | 1.00 | True | 29.637 | 0.363 |

