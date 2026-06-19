# 2022 Book Chapter - Container Transport Equations

Source file: `/Users/aayushjha/Downloads/2022'Book Chapter-ContrainerTransport.pdf`

Chapter title: "Energy-Efficient Scheduling of Intraterminal Container Transport"

Extraction status: the PDF has no extractable text layer. Equations below were transcribed from rendered page images. Page references use PDF page and printed page.

Important notation warning: in the loading-task model, constraint (15) is printed with `e_{ij} \ge 0`, even though the decision-variable list defines total energy as `\mathcal{E}`. This file preserves the printed equation and flags the likely notation inconsistency.

## Loading-Task MILP

Source: PDF pp.10-11 / printed pp.164-165.

### Objective Functions

Equation (1):

```latex
\begin{aligned}
\text{Minimize}\quad z_1 &= c_{\max},\\
z_2 &= \mathcal{E}.
\end{aligned}
```

### Assignment and Flow Constraints

Equation (2):

```latex
\sum_{i\in I}\sum_{j\in J_i}\sum_{v\in V} y_a^{ijv} \le 1,
\qquad \forall a \in A.
```

Equation (3):

```latex
\sum_{i\in I}\sum_{j\in J_i} w_{ij}
=
\sum_{a\in A}\sum_{i\in I}\sum_{j\in J_i}\sum_{v\in V} y_a^{ijv}.
```

Equation (4):

```latex
\sum_{k\in I\setminus\{i\}}\sum_{l\in J_k}\sum_{v\in V} x_{kl}^{ijv}
+
\sum_{\substack{l<j\\ l\in J_i}}\sum_{v\in V} x_{il}^{ijv}
+
\sum_{v\in V}\sum_{a\in A} y_a^{ijv}
= 1,
\qquad \forall i \in I;\ j \in J_i.
```

Equation (5):

```latex
\sum_{k\in I\setminus\{i\}}\sum_{l\in J_k}\sum_{v\in V} x_{ij}^{klv}
+
\sum_{\substack{l>j\\ l\in J_i}}\sum_{v\in V} x_{ij}^{ilv}
+
w_{ij}
= 1,
\qquad \forall i \in I;\ j \in J_i.
```

Equation (6):

```latex
\sum_{v\in V}\chi_{ij}^{v} = 1,
\qquad \forall i \in I;\ j \in J_i.
```

### Quay-Crane and Timing Constraints

Equation (7):

```latex
c_{ij} \ge c_{i(j-1)} + \tau_{ij},
\qquad \forall i \in I;\ j \in J_i\setminus\{1\}.
```

Equation (8):

```latex
c_{i1} \ge \tau_{i1},
\qquad \forall i \in I.
```

Equation (9):

```latex
c_{ij} \ge r_{ij} + \tau_{ij},
\qquad \forall i \in I;\ j \in J_i.
```

Equation (10):

```latex
r_{ij}
\ge
c_{kl}-\tau_{kl}
+
\theta_{kl}^{ijv}
+
\vartheta_{ij}^{\omega}
+
M\left(x_{kl}^{ijv}+\chi_{ij}^{\omega}-2\right),
```

```latex
\forall i,k \in I;\ j \in J_i;\ l \in J_k\ ( \text{if } i=k:\ j>l );
\ v,\omega \in V.
```

Equation (11):

```latex
r_{ij}
\ge
\theta_a^{ijv}
+
\vartheta_{ij}^{\omega}
+
M\left(y_a^{ijv}+\chi_{ij}^{\omega}-2\right),
\qquad
\forall i \in I;\ j \in J_i;\ a \in A;\ v,\omega \in V.
```

Equation (12):

```latex
c_{\max} \ge c_{in_i},
\qquad \forall i \in I.
```

### Energy Definition

Equation (13):

```latex
\mathcal{E}
=
\sum_{i\in I}\sum_{j\in J_i}
\left(
    \sum_{k\in I}\sum_{l\in J_k}\sum_{v\in V}
        \left(x_{kl}^{ijv}\theta_{kl}^{ijv}e^{v}\right)
    +
    \sum_{v\in V}
        \left(\chi_{ij}^{v}\vartheta_{ij}^{v}\varepsilon^{v}\right)
    +
    \sum_{a\in A}\sum_{v\in V}
        \left(y_a^{ijv}\theta_a^{ijv}e^{v}\right)
\right).
```

### Domains

Equation (14):

```latex
x_{kl}^{ijv},\ \chi_{ij}^{v},\ y_a^{ijv},\ w_{ij} \in \{0,1\},
\qquad
\forall i,k \in I;\ j \in J_i;\ l \in J_k;\ v \in V;\ a \in A.
```

Equation (15), printed literally:

```latex
c_{\max},\ c_{ij},\ r_{ij},\ e_{ij} \ge 0,
\qquad \forall i \in I;\ j \in J_i.
```

Likely intended energy-domain version:

```latex
c_{\max},\ c_{ij},\ r_{ij},\ \mathcal{E} \ge 0,
\qquad \forall i \in I;\ j \in J_i.
```

## Unloading-Task MILP Replacement Constraints

Source: PDF p.12 / printed p.166.

The chapter states that for unloading tasks, equations (1)-(8) remain and equations (13)-(15) remain; equations (9)-(12) are replaced by equations (16)-(19).

Equation (16):

```latex
c_{ij}
\ge
r_{kl}
+
\theta_{kl}^{ijv}
+
M\left(x_{kl}^{ijv}-1\right),
```

```latex
\forall i,k \in I;\ j \in J_i;\ l \in J_k\ ( \text{if } i=k:\ j>l );
\ v \in V.
```

Equation (17):

```latex
c_{ij}
\ge
\theta_a^{ijv}
+
M\left(y_a^{ijv}-1\right),
\qquad
\forall i \in I;\ j \in J_i;\ a \in A;\ v \in V.
```

Equation (18):

```latex
r_{ij}
\ge
c_{ij}
+
\vartheta_{ij}^{v}
+
M\left(\chi_{ij}^{v}-1\right),
\qquad
\forall i \in I;\ j \in J_i;\ v \in V.
```

Equation (19):

```latex
c_{\max} \ge r_{in_i},
\qquad \forall i \in I.
```

## Dual-Cycling MILP Replacement Constraints

Source: PDF pp.13-14 / printed pp.167-168.

The chapter states that dual-cycling uses equations (1)-(8) and (13)-(15), plus constraints (20)-(29).

Equation (20):

```latex
c_{ij} \ge r_{ij}+\tau_{ij},
\qquad \forall i \in I;\ j \in J_i;\ T_{ij}\in\mathcal{L}.
```

Equation (21):

```latex
r_{ij}
\ge
c_{kl}-\tau_{kl}
+
\theta_{kl}^{ijv}
+
\vartheta_{ij}^{\omega}
+
M\left(x_{kl}^{ijv}+\chi_{ij}^{\omega}-2\right),
```

```latex
\forall i,k \in I;\ j \in J_i;\ l \in J_k;\ v,\omega \in V;
T_{ij},T_{kl}\in\mathcal{L}.
```

Equation (22):

```latex
r_{ij}
\ge
\theta_a^{ijv}
+
\vartheta_{ij}^{\omega}
+
M\left(y_a^{ijv}+\chi_{ij}^{\omega}-2\right),
```

```latex
\forall i \in I;\ j \in J_i;\ a \in A;\ v,\omega \in V;
T_{ij}\in\mathcal{L}.
```

Equation (23):

```latex
c_{ij}
\ge
r_{kl}
+
\theta_{kl}^{ijv}
+
M\left(x_{kl}^{ijv}-1\right),
```

```latex
\forall i,k \in I;\ j \in J_i;\ l \in J_k;\ v \in V;
T_{ij},T_{kl}\in\mathcal{U}.
```

Equation (24):

```latex
c_{ij}
\ge
\theta_a^{ijv}
+
M\left(y_a^{ijv}-1\right),
\qquad
\forall i \in I;\ j \in J_i;\ a \in A;\ v \in V;
T_{ij}\in\mathcal{U}.
```

Equation (25):

```latex
r_{ij}
\ge
c_{ij}
+
\vartheta_{ij}^{v}
+
M\left(\chi_{ij}^{v}-1\right),
\qquad
\forall i \in I;\ j \in J_i;\ v \in V;
T_{ij}\in\mathcal{U}.
```

Equation (26):

```latex
c_{ij}
\ge
c_{kl}-\tau_{kl}
+
\theta_{kl}^{ijv}
+
M\left(x_{kl}^{ijv}-1\right),
```

```latex
\forall i,k \in I;\ j \in J_i;\ l \in J_k;\ v \in V;
T_{ij}\in\mathcal{U},\ T_{kl}\in\mathcal{L}.
```

Equation (27):

```latex
r_{ij}
\ge
r_{kl}
+
\theta_{kl}^{ijv}
+
\vartheta_{ij}^{\omega}
+
M\left(x_{kl}^{ijv}+\chi_{ij}^{\omega}-2\right),
```

```latex
\forall i,k \in I;\ j \in J_i;\ l \in J_k;\ v,\omega \in V;
T_{ij}\in\mathcal{L},\ T_{kl}\in\mathcal{U}.
```

Equation (28):

```latex
c_{\max} \ge c_{in_i},
\qquad \forall i \in I;\ T_{in_i}\in\mathcal{L}.
```

Equation (29):

```latex
c_{\max} \ge r_{in_i},
\qquad \forall i \in I;\ T_{in_i}\in\mathcal{U}.
```

## Reported GAP Formulas

Source: PDF p.21 / printed p.175 and PDF p.22 / printed p.176.

Equation (30):

```latex
GAP_{\mathcal{E}^{*}}
=
\frac{
    \mathcal{E}_{(\mathrm{Scen.}L\sim N)}^{*}
    -
    \mathcal{E}_{(\mathrm{Scen.}N)}^{*}
}{
    \mathcal{E}_{(\mathrm{Scen.}N)}^{*}
}
\times 100.
```

Equation (31):

```latex
GAP_{\mathcal{E}_{(D)}^{*}}
=
\frac{
    \mathcal{E}_{(D)}^{*}
    -
    \left(\mathcal{E}_{(L)}^{*}+\mathcal{E}_{(U)}^{*}\right)
}{
    \mathcal{E}_{(L)}^{*}+\mathcal{E}_{(U)}^{*}
}
\times 100.
```
