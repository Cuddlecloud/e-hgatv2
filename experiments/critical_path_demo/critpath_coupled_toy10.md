# Critical-path worked examples (R2)

## toy:10 (N=10, AGV=2, QC=3, coupled=True, fused R2(Cmax)=0.898)

### makespan_optimal: C_max=481.333, E=12270.833 (GNN C_max=591.609); leg-Jaccard(GNN vs oracle)=0.111; decomposition consistent (sum on-path = 481.333)

| order | task | activity | duration (exact) | dC_max | GNN on-path | GNN duration | abs err |
|---|---|---|---|---|---|---|---|
| 0 | t0 | empty_leg | 0.000 | 1.00 | True | 0.000 | 0.000 |
| 1 | t0 | loaded_leg | 41.667 | 1.00 | True | 46.334 | 4.667 |
| 2 | t0 | qc_handling | 73.000 | 1.00 | False | 72.697 | 0.303 |
| 3 | t5 | empty_leg | 16.667 | 1.00 | False | 14.715 | 1.951 |
| 4 | t5 | loaded_leg | 100.000 | 1.00 | False | 99.828 | 0.172 |
| 5 | t4 | empty_leg | 8.333 | 1.00 | False | 12.188 | 3.854 |
| 6 | t4 | loaded_leg | 100.000 | 1.00 | False | 91.789 | 8.211 |
| 7 | t9 | empty_leg | 41.667 | 1.00 | False | 41.320 | 0.347 |
| 8 | t9 | loaded_leg | 100.000 | 1.00 | False | 99.660 | 0.340 |

### energy_optimal: C_max=937.000, E=10804.167 (GNN C_max=967.992); leg-Jaccard(GNN vs oracle)=1.000; decomposition consistent (sum on-path = 937.000)

| order | task | activity | duration (exact) | dC_max | GNN on-path | GNN duration | abs err |
|---|---|---|---|---|---|---|---|
| 0 | t0 | empty_leg | 0.000 | 1.00 | True | 2.622 | 2.622 |
| 1 | t0 | loaded_leg | 62.500 | 1.00 | True | 61.381 | 1.119 |
| 2 | t0 | qc_handling | 73.000 | 1.00 | True | 72.697 | 0.303 |
| 3 | t6 | qc_handling | 33.000 | 1.00 | True | 32.490 | 0.510 |
| 4 | t3 | loaded_leg | 100.000 | 1.00 | True | 99.697 | 0.303 |
| 5 | t3 | qc_handling | 43.000 | 1.00 | True | 42.015 | 0.985 |
| 6 | t2 | empty_leg | 10.417 | 1.00 | True | 13.664 | 3.247 |
| 7 | t2 | loaded_leg | 62.500 | 1.00 | True | 60.488 | 2.012 |
| 8 | t2 | qc_handling | 56.000 | 1.00 | True | 55.190 | 0.810 |
| 9 | t5 | loaded_leg | 125.000 | 1.00 | True | 119.557 | 5.443 |
| 10 | t5 | qc_handling | 32.000 | 1.00 | True | 31.192 | 0.808 |
| 11 | t4 | empty_leg | 8.333 | 1.00 | True | 14.629 | 6.295 |
| 12 | t4 | loaded_leg | 125.000 | 1.00 | True | 114.348 | 10.652 |
| 13 | t4 | qc_handling | 45.000 | 1.00 | True | 44.263 | 0.737 |
| 14 | t7 | loaded_leg | 50.000 | 1.00 | True | 54.307 | 4.307 |
| 15 | t7 | qc_handling | 30.000 | 1.00 | True | 31.940 | 1.940 |
| 16 | t1 | empty_leg | 31.250 | 1.00 | True | 23.598 | 7.652 |
| 17 | t1 | loaded_leg | 50.000 | 1.00 | True | 56.917 | 6.917 |

