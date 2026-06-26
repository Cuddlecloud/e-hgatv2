# Critical-path worked examples (R2)

## toy:8 (N=8, AGV=2, QC=3, coupled=False, fused R2(Cmax)=0.998)

### makespan_optimal: C_max=350.444, E=10058.333 (GNN C_max=354.710); leg-Jaccard(GNN vs oracle)=1.000; decomposition consistent (sum on-path = 350.444)

| order | task | activity | duration (exact) | dC_max | GNN on-path | GNN duration | abs err |
|---|---|---|---|---|---|---|---|
| 0 | t5 | empty_leg | 34.722 | 1.00 | True | 44.166 | 9.444 |
| 1 | t5 | loaded_leg | 100.000 | 1.00 | True | 89.350 | 10.650 |
| 2 | t4 | empty_leg | 6.944 | 1.00 | True | 8.447 | 1.503 |
| 3 | t4 | loaded_leg | 83.333 | 1.00 | True | 83.805 | 0.471 |
| 4 | t2 | empty_leg | 27.778 | 1.00 | True | 30.578 | 2.800 |
| 5 | t2 | loaded_leg | 41.667 | 1.00 | True | 42.356 | 0.689 |
| 6 | t2 | qc_handling | 56.000 | 1.00 | True | 56.009 | 0.009 |

### energy_optimal: C_max=562.500, E=8631.250 (GNN C_max=566.527); leg-Jaccard(GNN vs oracle)=1.000; decomposition consistent (sum on-path = 562.500)

| order | task | activity | duration (exact) | dC_max | GNN on-path | GNN duration | abs err |
|---|---|---|---|---|---|---|---|
| 0 | t1 | empty_leg | 10.417 | 1.00 | True | 8.386 | 2.031 |
| 1 | t1 | loaded_leg | 62.500 | 1.00 | True | 62.895 | 0.395 |
| 2 | t0 | empty_leg | 0.000 | 1.00 | True | 2.130 | 2.130 |
| 3 | t0 | loaded_leg | 62.500 | 1.00 | True | 60.195 | 2.305 |
| 4 | t5 | empty_leg | 41.667 | 1.00 | True | 40.244 | 1.423 |
| 5 | t5 | loaded_leg | 125.000 | 1.00 | True | 128.557 | 3.557 |
| 6 | t4 | empty_leg | 10.417 | 1.00 | True | 19.378 | 8.962 |
| 7 | t4 | loaded_leg | 125.000 | 1.00 | True | 118.351 | 6.649 |
| 8 | t4 | qc_handling | 45.000 | 1.00 | True | 45.076 | 0.076 |
| 9 | t7 | loaded_leg | 50.000 | 1.00 | True | 51.175 | 1.175 |
| 10 | t7 | qc_handling | 30.000 | 1.00 | True | 30.141 | 0.141 |

