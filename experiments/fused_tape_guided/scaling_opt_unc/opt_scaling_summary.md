# R3 optimization scaling -- HV/HV* by N (mean +- 95% CI)

| Method | N=10 | N=20 | N=40 | N=80 |
|---|---|---|---|---|
| E-HGATv2-TAPE | 0.944±0.022 | 0.828±0.028 | 0.846±0.029 | 0.574±0.046 |
| E-HGATv2-attn | 0.929±0.028 | 0.804±0.030 | 0.870±0.026 | 0.617±0.038 |
| NSGA-II (random) | 0.843±0.032 | 0.608±0.057 | 0.578±0.034 | 0.149±0.041 |
| mp-BRKGA | 0.771±0.037 | 0.630±0.062 | 0.824±0.022 | 0.341±0.066 |
| single-pop BRKGA | 0.800±0.039 | 0.624±0.064 | 0.516±0.039 | 0.071±0.031 |

## HV/HV* gap: guided minus mp-BRKGA (positive = guided ahead)

| Guided arm | N=10 | N=20 | N=40 | N=80 |
|---|---|---|---|---|
| E-HGATv2-TAPE - mp-BRKGA | +0.173 | +0.198 | +0.022 | +0.233 |
| E-HGATv2-attn - mp-BRKGA | +0.158 | +0.174 | +0.045 | +0.276 |
