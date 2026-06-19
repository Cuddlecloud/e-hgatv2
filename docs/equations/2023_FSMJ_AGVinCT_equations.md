# 2023 FSMJ Journal - AGV in Container Terminals Equations

Source file: `/Users/aayushjha/Downloads/2023'FSMJ-Journal-AGVinCT.pdf`

Paper title: "A bi-objective multi-population biased random key genetic algorithm for joint scheduling quay cranes and speed adjustable vehicles in container terminals"

Extraction status: equations transcribed from rendered PDF pages and cross-checked against extracted text. Page references below use both PDF page and printed page where useful.

## Core Set Definition

Source: PDF p.8 / printed p.248.

The forbidden-pair set is printed as:

```latex
F =
\{(i,i), i \in J\}
\cup
\{(i,j) : j \le i,\ \text{with } i,j \in J_k \text{ and } k \in K\}.
```

Here \(J_k\) is the ordered set of tasks handled by quay crane \(k\), and \(J = \mathcal{L}\cup\mathcal{U}\).

## MILP Model

Source: PDF pp.8-10 / printed pp.248-250.

### Objective Functions

Equation (1):

```latex
\begin{aligned}
\text{Minimize}\quad Z_1 &= C_{\max},\\
Z_2 &= E.
\end{aligned}
```

### Makespan Definition

Equation (2):

```latex
C_{\max} \ge c_j, \qquad \forall j \in \mathcal{L}.
```

Equation (3):

```latex
C_{\max} \ge r_j, \qquad \forall j \in \mathcal{U}.
```

### Energy Definition

Equation (4):

```latex
E =
\sum_{j\in J}
\left(
    \sum_{i\in J}\sum_{v\in V}
        \left(x_{ij}^{v}\theta_{ij}^{v}e^{v}\right)
    +
    \sum_{v\in V}
        \left(\chi_{j}^{v}\vartheta_{j}^{v}\varepsilon^{v}\right)
    +
    \sum_{a\in A}\sum_{v\in V}
        \left(y_{aj}^{v}\theta_{aj}^{v}e^{v}\right)
\right).
```

### Assignment and Flow Constraints

Equation (5):

```latex
\sum_{j\in J}\sum_{v\in V} y_{aj}^{v} \le 1,
\qquad \forall a \in A.
```

Equation (6):

```latex
\sum_{j\in J} w_j
=
\sum_{a\in A}\sum_{j\in J}\sum_{v\in V} y_{aj}^{v}.
```

Equation (7):

```latex
\sum_{i\in J}\sum_{v\in V} x_{ij}^{v}
+
\sum_{v\in V}\sum_{a\in A} y_{aj}^{v}
= 1,
\qquad \forall j \in J.
```

Equation (8):

```latex
\sum_{i\in J}\sum_{v\in V} x_{ji}^{v} + w_j = 1,
\qquad \forall j \in J.
```

Equation (9):

```latex
\sum_{v\in V} \chi_j^{v} = 1,
\qquad \forall j \in J.
```

### Quay-Crane Precedence

Equation (10):

```latex
c_j \ge c_{j-1} + \tau_j,
\qquad \forall j \in J_k;\ k \in K.
```

### Loading-Task Timing Constraints

Equation (11):

```latex
c_j \ge r_j + \tau_j,
\qquad \forall j \in \mathcal{L}.
```

Equation (12):

```latex
r_j
\ge
c_i - \tau_i
+
\sum_{v\in V}\theta_{ij}^{v}x_{ij}^{v}
+
\sum_{\omega\in V}\vartheta_j^{\omega}\chi_j^{\omega}
+
M\left(\sum_{v\in V}x_{ij}^{v}-1\right),
\qquad \forall i,j \in \mathcal{L}.
```

Equation (13):

```latex
r_j
\ge
\sum_{v\in V}\theta_{aj}^{v}y_{aj}^{v}
+
\sum_{\omega\in V}\vartheta_j^{\omega}\chi_j^{\omega}
+
M\left(\sum_{v\in V}y_{aj}^{v}-1\right),
\qquad \forall j \in \mathcal{L};\ a \in A.
```

### Unloading-Task Timing Constraints

Equation (14):

```latex
c_j
\ge
r_i
+
\sum_{v\in V}\theta_{ij}^{v}x_{ij}^{v}
+
M\left(\sum_{v\in V}x_{ij}^{v}-1\right),
\qquad \forall i,j \in \mathcal{U}.
```

Equation (15):

```latex
c_j
\ge
\sum_{v\in V}\theta_{aj}^{v}y_{aj}^{v}
+
M\left(\sum_{v\in V}y_{aj}^{v}-1\right),
\qquad \forall j \in \mathcal{U};\ a \in A.
```

Equation (16):

```latex
r_j
\ge
c_j
+
\sum_{v\in V}\vartheta_j^{v}\chi_j^{v},
\qquad \forall j \in \mathcal{U}.
```

### Mixed Loading-Unloading Timing Constraints

Equation (17):

```latex
c_j
\ge
c_i - \tau_i
+
\sum_{v\in V}\theta_{ij}^{v}x_{ij}^{v}
+
M\left(\sum_{v\in V}x_{ij}^{v}-1\right),
\qquad \forall j \in \mathcal{U};\ i \in \mathcal{L}.
```

Equation (18):

```latex
r_j
\ge
r_i
+
\sum_{v\in V}\theta_{ij}^{v}x_{ij}^{v}
+
\sum_{\omega\in V}\vartheta_j^{\omega}\chi_j^{\omega}
+
M\left(\sum_{v\in V}x_{ij}^{v}-1\right),
\qquad \forall j \in \mathcal{L};\ i \in \mathcal{U}.
```

### Domains

Equation (19):

```latex
x_{ij}^{v},\ \chi_j^{v},\ y_{aj}^{v},\ w_j \in \{0,1\},
\qquad \forall i,j \in J;\ v \in V;\ a \in A.
```

Equation (20):

```latex
C_{\max},\ c_j,\ r_j,\ E \ge 0,
\qquad \forall j \in J.
```

## Crowding Distance and Performance Indicators

Source: PDF p.13 / printed p.253 and PDF p.16 / printed p.256.

The text defines total crowding distance as:

```latex
CD_l = \sum_{\omega=1}^{\Omega} CD_l^{\omega}.
```

Equation (21):

```latex
CD_l^{\omega}
=
\frac{f_{l+1}^{\omega}-f_{l-1}^{\omega}}
     {f_{\max}^{\omega}-f_{\min}^{\omega}}.
```

Equation (22):

```latex
GD^{+}(PF)
=
\frac{1}{n}
\sum_{i=1}^{n}
\left(
    \min_{j\in PF^{*}}\left\{d_{(i,j)}^{+}\right\}
\right),
```

with:

```latex
d_{(i,j)}^{+}
=
\sqrt{
    \left(\max\left\{f_1^{i}-f_1^{j},0\right\}\right)^2
    +
    \left(\max\left\{f_2^{i}-f_2^{j},0\right\}\right)^2
}.
```

Equation (23):

```latex
\Delta(PF)
=
\frac{
    d_u+d_b+\sum_{i=1}^{n-1}\left|d_i-\bar{d}\right|
}{
    d_u+d_b+\bar{d}(n-1)
}.
```

Equation (24):

```latex
f_1^{N}
=
\frac{f_1-f_1^{\min}}{f_1^{\max}-f_1^{\min}},
\qquad
f_2^{N}
=
\frac{f_2-f_2^{\min}}{f_2^{\max}-f_2^{\min}}.
```

## Reported Deviation Formulas

Source: PDF p.19 / printed p.259.

The paper reports average percentage deviations for the boundary solutions as:

```latex
\delta_C
=
\frac{C_{\max}-C_{\max}^{*}}{C_{\max}^{*}}
\times 100,
\qquad
\delta_E
=
\frac{E-E^{*}}{E^{*}}
\times 100.
```

