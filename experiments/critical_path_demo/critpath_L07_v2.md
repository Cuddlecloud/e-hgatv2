# Critical-path worked examples (R2)

## L07 (N=8, AGV=2, QC=2, coupled=False, fused R2(Cmax)=1.000)

### makespan_optimal: C_max=385.389, E=10316.667 (GNN C_max=386.051); leg-Jaccard(GNN vs oracle)=1.000; decomposition consistent (sum on-path = 385.389)

| order | task | activity | duration (exact) | dC_max | GNN on-path | GNN duration | abs err |
|---|---|---|---|---|---|---|---|
| 0 | t0 | empty_leg | 41.667 | 1.00 | True | 41.486 | 0.181 |
| 1 | t0 | loaded_leg | 41.667 | 1.00 | True | 41.648 | 0.019 |
| 2 | t2 | empty_leg | 33.333 | 1.00 | True | 31.706 | 1.628 |
| 3 | t2 | loaded_leg | 55.556 | 1.00 | True | 57.774 | 2.219 |
| 4 | t3 | empty_leg | 20.833 | 1.00 | True | 22.351 | 1.517 |
| 5 | t3 | loaded_leg | 50.000 | 1.00 | True | 47.745 | 2.255 |
| 6 | t1 | empty_leg | 27.778 | 1.00 | True | 33.524 | 5.746 |
| 7 | t1 | loaded_leg | 55.556 | 1.00 | True | 50.669 | 4.886 |
| 8 | t1 | qc_handling | 59.000 | 1.00 | True | 59.149 | 0.149 |

### energy_optimal: C_max=853.917, E=9100.000 (GNN C_max=853.992); leg-Jaccard(GNN vs oracle)=1.000; decomposition consistent (sum on-path = 853.917)

| order | task | activity | duration (exact) | dC_max | GNN on-path | GNN duration | abs err |
|---|---|---|---|---|---|---|---|
| 0 | t7 | empty_leg | 50.000 | 1.00 | True | 55.581 | 5.581 |
| 1 | t7 | loaded_leg | 83.333 | 1.00 | True | 78.382 | 4.951 |
| 2 | t6 | empty_leg | 31.250 | 1.00 | True | 27.257 | 3.993 |
| 3 | t6 | loaded_leg | 50.000 | 1.00 | True | 54.214 | 4.214 |
| 4 | t1 | empty_leg | 25.000 | 1.00 | True | 25.244 | 0.244 |
| 5 | t1 | loaded_leg | 66.667 | 1.00 | True | 65.334 | 1.333 |
| 6 | t3 | empty_leg | 31.250 | 1.00 | True | 31.600 | 0.350 |
| 7 | t3 | loaded_leg | 62.500 | 1.00 | True | 63.120 | 0.620 |
| 8 | t0 | empty_leg | 25.000 | 1.00 | True | 26.866 | 1.866 |
| 9 | t0 | loaded_leg | 62.500 | 1.00 | True | 61.735 | 0.765 |
| 10 | t5 | empty_leg | 25.000 | 1.00 | True | 30.798 | 5.798 |
| 11 | t5 | loaded_leg | 83.333 | 1.00 | True | 75.635 | 7.698 |
| 12 | t4 | empty_leg | 25.000 | 1.00 | True | 29.257 | 4.257 |
| 13 | t4 | loaded_leg | 62.500 | 1.00 | True | 58.267 | 4.233 |
| 14 | t2 | empty_leg | 31.250 | 1.00 | True | 28.543 | 2.707 |
| 15 | t2 | loaded_leg | 83.333 | 1.00 | True | 85.830 | 2.496 |
| 16 | t2 | qc_handling | 56.000 | 1.00 | True | 56.329 | 0.329 |

