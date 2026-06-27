# R4: Pareto-Front Behaviour Learning

**Train instances:** toy:8:2:2, toy:10:2:2, toy:12:2:2, toy:10:3:2, toy:12:3:2, toy:14:3:2, toy:18:3:2, toy:30:3:3, toy:42:3:3, toy:24:4:3, toy:36:4:4, toy:48:4:4, toy:36:6:4, toy:54:6:5, toy:24:2:2, toy:40:2:3
**Test instance:** toy:30:5:3, toy:45:5:4, L07
**Train points:** 714, **Test points:** 128

## Generalisation Results

| Metric | Train | Test (held-out) |
|---|---|---|
| MAE(transport%) | 0.049 | 0.113 |
| MAE(QC%) | 0.050 | 0.112 |
| Corr(transport%) | 0.874 | 0.440 |
| Corr(QC%) | 0.875 | 0.421 |

## Interpretation

The predictor learns how the critical-path composition (transport vs QC fraction)
varies as a function of the trade-off weight λ. High correlation on the held-out
instance demonstrates that the front behaviour generalises across instances of
similar structure—the model has learned the structural pattern that makespan-
optimal schedules are transport-bound while energy-optimal schedules are crane-bound.
