# mp-BRKGA fidelity diff

Our `src/ehgat/baselines/mp_brkga.py` against the author's own `large/mp-BRKGA_DL01.py`.
Written **before** any edit, so the diff is the specification rather than a post-hoc rationalisation.

His configuration, read from the source: `REP=2`, `eliten=0.2`, `tossn=0.7`, `Mutrate=0.1`,
`nPOP=4` (Ω=2 single-objective + Π=2 multi-objective), `Gmax=300`, `nex=30`, `Scenario=3`,
`A=4`; `N=sum(J)` at `:131`; `Pmax=20*N` at `:132`; `Mutant=ceil(Mutrate*Pmax)` at `:137`;
`elite=ceil(eliten*Pmax)` at `:138`; `rank=0` (crowding distance, not pure dominance) at `:31`.

## Verdict summary

| # | area | his location | ours | class |
|---|---|---|---|---|
| 1 | makespan definition | `:239-240` | `evaluator.py:232`, `:433` | **identical — verified** |
| 2 | mutant gene structure | `:252-254` | `mp_brkga.py:172` | **substantive** |
| 3 | second-parent pool | `:264` | `mp_brkga.py:163` | **substantive** |
| 4 | elite/mutant rounding | `:137-138` | `mp_brkga.py:216-217` | **substantive (minor)** |
| 5 | block layout | `popNEW` writes | `mp_brkga.py:156,168,172` | inert |
| 6 | spread metric Δ | `:640-662` | not in `mp_brkga.py` | **substantive (reporting)** |
| 7 | toss comparison | `:265-268` | `mp_brkga.py:124` | inert |

---

## 1. Makespan definition — IDENTICAL, no change needed

His objective is split across two arrays:

```python
Cmax = max(C)          # per-task QC completion
Rmax = max(AGV1)       # per-vehicle availability
Obj[nn, i, 0] = max(Cmax, Rmax)
```

Ours is a single maximum, `makespan = max(completion)`.

**These are equal, not approximately equal.** His `AGV1[a]` is exactly our `agv_free_after[j]`:

- **LOAD** (`:209-210`, `:224-226`): `AGV1[a]` is assigned *before* the crane lifts, so
  `AGV1 = C[T] - tau`, always dominated by `Cmax`.
- **UNLOAD** (`:217-218`, `:233-234`): `AGV1[a] = C[T] + TrL*R[w] = r_j`. His `Cmax` uses
  `C[T]`, which excludes the loaded leg; `Rmax` supplies `r_j`. Our
  `completion[j] = arr_dropoff[j] = r_j` includes it directly.

The asymmetry of Eq (2) (`Cmax ≥ c_j`, LOAD) and Eq (3) (`Cmax ≥ r_j`, UNLOAD) is what makes
this work.

**Verified empirically:** 2400 random schedules over L01/L07/L15/L21/L35 and
DL01/DL05/DL10 — `max|his − ours| == 0` exactly, zero differing cases.

## 2. Mutant gene structure — SUBSTANTIVE

His mutants are **block-typed**, not uniform random keys:

```python
popNEW[0:N,     elite:elite+Mutant] = random.rand(N, Mutant)          # continuous priorities
popNEW[N:3*N,   elite:elite+Mutant] = random.randint(V, size=(2*N, Mutant))  # speed levels
popNEW[3*N:4*N, elite:elite+Mutant] = random.randint(A, size=(N, Mutant))    # AGV index
```

Ours generates uniform `[0,1)` across all `4N` genes:

```python
nxt[n_elite + n_offspring :] = rng.random((n_mutant, chrom_len))   # mp_brkga.py:172
```

**His chromosome is therefore not all random keys.** Blocks 2–4 hold integers directly, and only
block 1 is a random key. Two consequences beyond the operator itself:

- the decoder's interpretation of blocks 2–4 differs in kind, not just in distribution;
- the `4N` vector is also the XGBoost baseline's feature vector, so the baseline's feature
  semantics change with it.

## 3. Second-parent pool — SUBSTANTIVE

```python
P1 = random.randint(0, elite)      # :263  first parent among the elites
P2 = random.randint(elite, Pmax)   # :264  second parent among the NON-elites
```

Ours draws the second parent from the **entire** population:

```python
op = pop[rng.integers(pop.shape[0])]   # mp_brkga.py:163
```

So ours can pair two elites; his cannot. This reduces our effective diversity pressure relative to
his, mildly.

## 4. Elite/mutant rounding — SUBSTANTIVE (minor)

His: `Mutant = math.ceil(Mutrate*Pmax)`, `elite = math.ceil(eliten*Pmax)`.
Ours: `round(...)` at `mp_brkga.py:216-217`.

At `Pmax = 20N` both agree whenever `0.2*Pmax` and `0.1*Pmax` are integral, which holds for
every `N` since `20N*0.2 = 4N` and `20N*0.1 = 2N`. **So for his published `Pmax = 20N` the two
are identical**; they diverge only if `pop_size` is overridden to a value where the products are
fractional. Worth aligning for exactness, but it cannot explain any observed difference at the
published configuration.

## 5. Block layout — INERT

His order within `popNEW` is **elite, mutant, offspring**; ours is **elite, offspring, mutant**
(`mp_brkga.py:156`, `:168`, `:172`).

Selection re-sorts the population every generation, so position carries no information and the
resulting distribution is unchanged. It does change the RNG consumption order, so
seed-for-seed reproduction of his exact trajectory is impossible without matching it.
**Recommendation: do not change** on cosmetic grounds; record the reason.

## 6. Spread metric Δ — SUBSTANTIVE for reporting only

His Δ at `:640-662` computes consecutive-neighbour distances `dd[i,0]`, their mean `dd[-1,0]`,
the absolute deviations `dd[i,1]`, and then

```python
db = 0
du = 0
SP[repeat] = (du + db + dd[-1,1]) / (du + db + dd[-1,0]*(len(ObjFinalN)-1))
```

The standard Deb Δ includes the distances from the extreme found solutions to the true extremes
in both numerator and denominator; **his sets both to zero**. Any Δ compared against his
published values must use his definition, or the comparison is meaningless. This affects
reporting, not the algorithm.

## 7. Toss comparison — INERT

His `popNEW[toss <= tossn] = Par1` inherits the elite gene when `toss <= tossn`; ours uses
`rng.random(...) < inherit_prob` (`mp_brkga.py:124`). The boundary case has measure zero on
continuous draws. **No change.**

---

## Recommended edits, smallest first

1. **(4)** `round` → `math.ceil` in `mp_brkga.py:216-217`. One line; no behavioural change at
   `Pmax = 20N`, but removes a latent divergence.
2. **(3)** restrict the second parent to non-elites at `mp_brkga.py:163`. Requires knowing the
   elite boundary inside `_breed`, which it already receives as `n_elite`.
3. **(2)** block-typed mutant generation. The largest change, and the one that touches the
   decoder contract — it should be done with a test asserting the block ranges, and its effect on
   the XGBoost baseline's feature vector noted.

Leave (1), (5), (6), (7) alone: (1) is already correct, (5) and (7) are inert, and (6) belongs in the
reporting layer rather than in the optimiser.
