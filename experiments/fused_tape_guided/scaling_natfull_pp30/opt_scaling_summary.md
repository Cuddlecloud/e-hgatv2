# R3 optimization scaling -- HV/HV* by N (mean +- 95% CI)

| Method | N=10 | N=20 | N=40 | N=80 |
|---|---|---|---|---|
| E-HGATv2-TAPE | 0.925±0.043 | 0.882±0.067 | 0.774±0.086 | 0.831±0.062 |
| E-HGATv2-attn | 0.911±0.074 | 0.815±0.102 | 0.808±0.095 | 0.772±0.080 |
| NSGA-II (random) | 0.764±0.112 | 0.589±0.127 | 0.493±0.097 | 0.446±0.075 |
| mp-BRKGA | 0.774±0.086 | 0.712±0.119 | 0.858±0.083 | 0.774±0.102 |
| single-pop BRKGA | 0.852±0.041 | 0.734±0.038 | 0.442±0.064 | 0.353±0.089 |

## HV/HV* gap: guided minus mp-BRKGA (positive = guided ahead)

| Guided arm | N=10 | N=20 | N=40 | N=80 |
|---|---|---|---|---|
| E-HGATv2-TAPE - mp-BRKGA | +0.151 | +0.170 | -0.084 | +0.057 |
| E-HGATv2-attn - mp-BRKGA | +0.136 | +0.102 | -0.050 | -0.002 |
