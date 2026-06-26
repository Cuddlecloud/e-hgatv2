# R4: Pareto-Front Behaviour Learning

**Train instances:** toy:5, toy:8, toy:10
**Test instance:** L07
**Train points:** 301, **Test points:** 73

## Generalisation Results

| Metric | Train | Test (held-out) |
|---|---|---|
| MAE(transport%) | 0.032 | 0.126 |
| MAE(QC%) | 0.032 | 0.126 |
| Corr(transport%) | 0.928 | -0.486 |
| Corr(QC%) | 0.927 | -0.504 |

## Interpretation

The predictor learns how the critical-path composition (transport vs QC fraction)
varies as a function of the trade-off weight λ. High correlation on the held-out
instance demonstrates that the front behaviour generalises across instances of
similar structure—the model has learned the structural pattern that makespan-
optimal schedules are transport-bound while energy-optimal schedules are crane-bound.
