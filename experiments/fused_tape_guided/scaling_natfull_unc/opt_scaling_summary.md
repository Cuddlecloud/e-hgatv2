# R3 optimization scaling -- HV/HV* by N (mean +- 95% CI)

| Method | N=10 | N=20 | N=40 | N=80 |
|---|---|---|---|---|
| E-HGATv2-TAPE | 0.912±0.048 | 0.929±0.049 | 0.849±0.045 | 0.832±0.057 |
| E-HGATv2-attn | 0.929±0.034 | 0.879±0.059 | 0.851±0.066 | 0.859±0.106 |
| NSGA-II (random) | 0.825±0.054 | 0.799±0.091 | 0.659±0.040 | 0.575±0.103 |
| mp-BRKGA | 0.768±0.089 | 0.838±0.083 | 0.890±0.050 | 0.773±0.063 |
| single-pop BRKGA | 0.848±0.068 | 0.773±0.132 | 0.570±0.058 | 0.455±0.074 |

## HV/HV* gap: guided minus mp-BRKGA (positive = guided ahead)

| Guided arm | N=10 | N=20 | N=40 | N=80 |
|---|---|---|---|---|
| E-HGATv2-TAPE - mp-BRKGA | +0.144 | +0.091 | -0.041 | +0.059 |
| E-HGATv2-attn - mp-BRKGA | +0.161 | +0.041 | -0.040 | +0.086 |
