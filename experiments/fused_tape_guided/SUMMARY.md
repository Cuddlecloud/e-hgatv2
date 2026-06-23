# Faithful-guidance study — consolidated results (Req 2 + Req 3)

_5 seeds/instance, 40 gens, matched exact-eval budget (P = 5·N per population; GAT/BRKGA
pop = 4P). Reference PF\*: exact Oracle for toy:5, else non-dominated union of mp-BRKGA +
BRKGA + TAPE @ 50 gens. All 11 configs complete._

## HV / HV\* (higher = better) and guidance faithfulness

| Instance | N | regime | TAPE | attn | random | mp-BRKGA | sp-BRKGA | TAPE leg-Jaccard | attn ρ |
|---|---|---|---|---|---|---|---|---|---|
| toy:5  | 5  | unc | 0.978 | 0.965 | 0.981 | 0.934 | 0.976 | 0.980 | 0.070 |
| toy:8  | 8  | unc | 0.942 | 0.961 | 0.924 | 0.902 | 0.905 | 0.990 | −0.008 |
| toy:10 | 10 | unc | 0.948 | 1.003 | 0.925 | 0.886 | 0.953 | 0.975 | 0.088 |
| toy:15 | 15 | unc | 0.832 | 0.869 | 0.774 | 0.748 | 0.794 | 0.991 | 0.069 |
| toy:20 | 20 | unc | 0.931 | 0.957 | 0.810 | 0.890 | 0.832 | 0.949 | 0.016 |
| L07    | 8  | unc | 0.973 | 0.978 | 0.965 | 0.895 | 0.950 | 0.985 | 0.171 |
| L15    | 16 | unc | 0.959 | 0.953 | 0.894 | 0.874 | 0.891 | 0.996 | 0.081 |
| L21    | 12 | unc | 1.014 | 0.985 | 0.938 | 0.842 | 0.955 | 0.988 | 0.057 |
| L35    | 12 | unc | 0.986 | 0.993 | 0.944 | 0.930 | 0.933 | 1.000 | 0.085 |
| toy:10 | 10 | **coupled** | 0.859 | 0.919 | 0.741 | 0.798 | 0.791 | 0.952 | −0.087 |
| toy:20 | 20 | **coupled** | 0.846 | 0.883 | 0.697 | 0.767 | 0.821 | 0.874 | −0.035 |

## What the data supports (honest)

1. **Req 2 — TAPE is faithful, attention is not (clean win).** TAPE leg-critical Jaccard
   vs the exact oracle is **0.95–1.00 on every instance**; attention's Spearman ρ with the
   true per-task makespan levers is **≈ 0** (−0.09 to 0.17) — i.e. attention does *not* rank
   the bottlenecks. This is the novelty and it is solid.

2. **Req 3 — GNN guidance beats the metaheuristics.** Both GNN-guided arms (TAPE and attn)
   beat **mp-BRKGA, single-pop BRKGA, and random** on HV/HV\* in 9/10 instances (N=5 is not
   discriminative — everything is near-optimal). mp-BRKGA is consistently the **weakest** on
   GD+/IGD+. The GNN-vs-mp-BRKGA gap is often statistically significant (non-overlapping 95%
   CIs, e.g. L21, L15, toy:15).

## What the data does NOT support (the part to be honest about)

3. **TAPE does NOT beat attention on optimization.** They are statistically
   indistinguishable (overlapping CIs at 5 seeds), and attention is numerically ahead more
   often (toy:8/10/15/20, L07, L35, coupled). So the hypothesis "TAPE guidance converges
   *faster* / beats attention" is **not** evidenced here.

   The defensible claim is therefore the weaker-but-true one: **routing guidance through the
   faithful TAPE signal preserves the optimization win** (it matches the unfaithful attention
   signal) — so faithfulness is obtained *for free*, the same object both explains (Req 2)
   and competently steers (Req 3). We cannot claim the faithful signal steers *better*.

4. **Coupled regime is weaker.** At N=10 coupled TAPE (0.86) < attn (0.92), and at N=20 coupled
   TAPE (0.85) < attn (0.88) — but both GNN arms still beat random/mp-BRKGA/sp-BRKGA. TAPE
   leg-Jaccard also drops in coupled (0.87 at N=20 vs 0.95–1.0 uncoupled) and the coupled fused
   R² was only ~0.80 (vs 0.99 uncoupled) with TAPE makespan abs-error ~61 vs oracle — the
   unrolled wait-head needs more samples/epochs/unroll before the coupled TAPE claim is strong.

## Caveats / to strengthen before submission

- **Reference proxy is approximate** — some HV/HV\* > 1.0 (toy:10 attn, L21 TAPE) means a
  40-gen run beat the 50-gen PF\* union. Rebuild PF\* at higher gens (e.g. 300) for the paper.
- **5 seeds → wide CIs.** Bump to 15–30 seeds to tighten and to test TAPE-vs-attn / GNN-vs-mp
  significance with Wilcoxon + Holm.
- **Budget is P=5N (not the paper's 20N)** for tractability; re-run the headline at 20N once
  the TAPE screening/signals are GPU-batched (currently per-graph on CPU).
