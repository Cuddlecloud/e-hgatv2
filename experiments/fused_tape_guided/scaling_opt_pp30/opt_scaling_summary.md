# R3 optimization scaling -- HV/HV* by N (mean +- 95% CI)

| Method | N=10 | N=20 | N=40 | N=80 |
|---|---|---|---|---|
| E-HGATv2-TAPE | 0.871±0.038 | 0.826±0.051 | 0.876±0.036 | 0.823±0.029 |
| E-HGATv2-attn | 0.864±0.035 | 0.812±0.045 | 0.869±0.035 | 0.788±0.031 |
| NSGA-II (random) | 0.765±0.048 | 0.462±0.063 | 0.440±0.054 | 0.338±0.057 |
| mp-BRKGA | 0.732±0.040 | 0.635±0.065 | 0.752±0.034 | 0.500±0.065 |
| single-pop BRKGA | 0.756±0.041 | 0.574±0.084 | 0.432±0.049 | 0.285±0.055 |

## HV/HV* gap: guided minus mp-BRKGA (positive = guided ahead)

| Guided arm | N=10 | N=20 | N=40 | N=80 |
|---|---|---|---|---|
| E-HGATv2-TAPE - mp-BRKGA | +0.140 | +0.191 | +0.123 | +0.323 |
| E-HGATv2-attn - mp-BRKGA | +0.133 | +0.177 | +0.117 | +0.288 |
