# Critical-path worked examples (R2)

## L07 (N=8, AGV=2, QC=2, coupled=False, fused R2(Cmax)=1.000)

### makespan_optimal: C_max=384.056, E=10308.333 (GNN C_max=384.303); leg-Jaccard(GNN vs oracle)=1.000; decomposition consistent (sum on-path = 384.056)

| order | task | activity | duration (exact) | dC_max | GNN on-path | GNN duration | abs err |
|---|---|---|---|---|---|---|---|
| 0 | t5 | empty_leg | 41.667 | 1.00 | True | 45.307 | 3.640 |
| 1 | t5 | loaded_leg | 66.667 | 1.00 | True | 62.230 | 4.437 |
| 2 | t6 | empty_leg | 20.833 | 1.00 | True | 23.226 | 2.393 |
| 3 | t6 | loaded_leg | 50.000 | 1.00 | True | 47.502 | 2.498 |
| 4 | t6 | qc_handling | 78.000 | 1.00 | True | 78.044 | 0.044 |
| 5 | t7 | empty_leg | 33.333 | 1.00 | True | 32.887 | 0.447 |
| 6 | t7 | loaded_leg | 55.556 | 1.00 | True | 56.883 | 1.327 |
| 7 | t7 | qc_handling | 38.000 | 1.00 | True | 38.224 | 0.224 |

### energy_optimal: C_max=895.583, E=9050.000 (GNN C_max=893.251); leg-Jaccard(GNN vs oracle)=1.000; decomposition consistent (sum on-path = 895.583)

| order | task | activity | duration (exact) | dC_max | GNN on-path | GNN duration | abs err |
|---|---|---|---|---|---|---|---|
| 0 | t0 | empty_leg | 62.500 | 1.00 | True | 60.611 | 1.889 |
| 1 | t0 | loaded_leg | 62.500 | 1.00 | True | 64.421 | 1.921 |
| 2 | t7 | empty_leg | 25.000 | 1.00 | True | 27.984 | 2.984 |
| 3 | t7 | loaded_leg | 83.333 | 1.00 | True | 80.023 | 3.311 |
| 4 | t1 | empty_leg | 31.250 | 1.00 | True | 32.082 | 0.832 |
| 5 | t1 | loaded_leg | 83.333 | 1.00 | True | 82.501 | 0.833 |
| 6 | t3 | empty_leg | 31.250 | 1.00 | True | 26.524 | 4.726 |
| 7 | t3 | loaded_leg | 50.000 | 1.00 | True | 54.960 | 4.960 |
| 8 | t5 | empty_leg | 31.250 | 1.00 | True | 34.955 | 3.705 |
| 9 | t5 | loaded_leg | 83.333 | 1.00 | True | 78.612 | 4.721 |
| 10 | t6 | empty_leg | 25.000 | 1.00 | True | 28.636 | 3.636 |
| 11 | t6 | loaded_leg | 62.500 | 1.00 | True | 57.977 | 4.523 |
| 12 | t4 | empty_leg | 31.250 | 1.00 | True | 31.529 | 0.279 |
| 13 | t4 | loaded_leg | 62.500 | 1.00 | True | 61.870 | 0.630 |
| 14 | t2 | empty_leg | 31.250 | 1.00 | True | 28.655 | 2.595 |
| 15 | t2 | loaded_leg | 83.333 | 1.00 | True | 85.897 | 2.564 |
| 16 | t2 | qc_handling | 56.000 | 1.00 | True | 56.013 | 0.013 |

