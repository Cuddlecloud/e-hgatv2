# Study plan — from fuzzy to defensible

Preparation for the in-person presentation to Prof. Homayouni. The ordering is by
question-probability, not by the structure of the paper: the material most likely to be
asked about comes first, so that an interruption to the schedule degrades the outcome
gracefully.

Two targets are separated deliberately.

- **Part 1 (Days 1–3, ~18 h)** — defensible on the questions he is likely to ask.
- **Part 2 (Days 4–7, ~25 h)** — full command of the paper and the code.

Every block ends in a **self-test**: a question to be answered aloud, without notes,
before the block is counted as done. Reading without the self-test does not transfer.

---

## Part 1 — Meeting-critical

### Day 1 — The problem and the recurrence (6 h)

**1.1 The problem as he states it (2 h).**
`2023'FSMJ-Journal-AGVinCT.pdf` §1–3 and `2022'Book Chapter-ContrainerTransport.pdf`.
Read for four things only: the four subproblems, the two objectives, what a LOAD and an
UNLOAD task each consist of, and the fact that the energy objective covers AGV travel and
not crane handling.

**1.2 The recurrence by hand (3 h). This is the highest-value block in the plan.**
`paper/main.tex:150-212`. Take L01 from `data/tables_4_5.json` — four tasks, two AGVs.
On paper: fix an assignment and a sequence, pick speed levels, and compute every $c_j$ by
hand using the two completion equations at `:190` and `:196`. Then take
$C_{\max}=\max_j c_j$ and trace backwards which activities bind it.

Check the hand result against the code:

```
.venv/bin/python -c "
import sys; sys.path.insert(0,'src')
from ehgat.environment.dsdl import load_tables_4_5
inst = load_tables_4_5('data/tables_4_5.json', only=['L01'])[0].instance
print(len(inst.tasks), inst.num_agvs)
"
```

then evaluate the same schedule through `ehgat.environment.evaluator.evaluate` and confirm
the makespan matches, and `ehgat.benchmark.faithfulness.critical_path_binding` and confirm
the binding tasks match what you traced. That function returns `(agv_bound, qc_bound)`, two
disjoint sets partitioning the critical-path tasks by which resource gates them, so it tells
you not only which tasks bind but whether each is held by its vehicle or by its crane.

**1.3 Why this is max-plus (1 h).** `paper/main.tex:199-212`. Every completion is a maximum
of sums, so the makespan is a longest path in the precedence graph under $(\max,+)$.
Understand why that makes the objective a function of the activities on one path, and why
that path can change discontinuously when a decision changes.

> **Self-test.** On a blank sheet: draw the precedence graph for a four-task instance,
> compute the makespan, mark the critical path, and state what happens to $C_{\max}$ if a
> single leg on that path is lengthened by $\Delta$ — and if a leg off it is.

### Day 2 — What is learned, what is computed, and his baseline (6 h)

**2.1 The division of labour (2 h).** `paper/main.tex:533-674` and
`src/ehgat/explain/fused_ehgat.py:1-60`. Establish precisely: the two completion
recurrences, $C_{\max}=\max_j c_j$, and $E=\sum_j(e^{\text{empty}}_j+e^{\text{loaded}}_j)$
are computed, never learned. The per-leg times and energies and the handling delay $\tau$
are learned, and are anchored during training against their exact physical values. The
coupled power-wait is learned and has no closed form.

**2.2 Why the gradient is binary (1 h).** `paper/main.tex:734-830`,
`src/ehgat/explain/fused_explainer.py`. The subgradient of a max selects the argmax, so
$\partial C_{\max}/\partial(\text{leg})$ is an indicator of critical-path membership. This
is the reason the recurrence is embedded rather than regressed; the fidelity is a
by-product.

**2.3 The two TAPEs (1 h).** `src/ehgat/explain/tape_explainer.py` is the exact oracle and
uses no network. `src/ehgat/explain/fused_explainer.py` differentiates the model with
respect to its own predicted legs and is what guides the search. Know which is which and
why the separation is what keeps the faithfulness result from being circular.

**2.4 His own method as the baseline (2 h).** `Homayouni_XAI+MOO.pdf` p.2,
`src/ehgat/surrogate/explainer_xgb.py`, `paper/main.tex:1940-2013`, `tab:xgb` at `:1988`.
Be able to state the three reasons in §1951, §1962 and §1970 and the numbers attached to
each: held-out $R^2$ 0.12 and 0.27 against 0.997 and 1.000; TreeSHAP attributing to
decision variables rather than to physical quantities; and the Sobol decomposition giving
first-order indices of 0.00 against total-order 0.71 and 0.72.

> **Self-test.** Answer both aloud. *"Why is embedding the recurrence not simply building
> in the answer?"* and *"You could have used my XGBoost and TreeSHAP approach — why
> didn't you?"* The second must include the $R^2$ figures and must concede that the
> comparison is between inductive biases and not between learning capacities.

### Day 3 — The results (6 h)

**3.1 mp-BRKGA (2 h).** `src/ehgat/baselines/mp_brkga.py` beside his parameter table.
Confirm for yourself which of his operators are present — biased parameterised uniform
crossover, elite and mutant fractions, the $\Omega$ and $\Pi$ populations, elite exchange
— and be ready to say plainly that the generation budget is smaller than his 300 and that
every arm in the comparison shares that reduced budget.

**3.2 The headline (2 h).** `paper/main.tex:1524-1552` with `tab:main` at `:1773`, plus the
statistical protocol at `:1829` with `tab:stats` and `tab:boot`. For each number: what was
run, how many seeds, what the reference point is, and what the caveat is.

**3.3 Scaling and generalisation (1 h).** `paper/main.tex:1174-1238` with `tab:generalize`,
and `:1553-1750` with `tab:optladder`. The claim that carries the OR value is that the
advantage holds as $N$ grows where mp-BRKGA and random NSGA-II stall.

**3.4 The front, and yesterday's transfer result (1 h).** `paper/main.tex:2014-2115` and
`:2116-2246` with `tab:pts` and `tab:amortise`, then `experiments/front_transfer/summary.json`.
Know that the transferred surrogate recovers 0.9969 of the true front's hypervolume against
a 0.8469 floor and sits 0.0030 below refitting, that the search-provenance contrast is not
resolvable at these instance sizes because the test saturates, and that the migration
measure is not quotable until its definition is reconciled.

> **Self-test.** Pick any three numbers in `tab:main` at random and state, without looking:
> what was run to produce them, what the control was, and what the honest caveat is.

---

## Part 2 — Full command

### Day 4 — The rest of the method (6 h)

- Decision variables and the search space, `paper/main.tex:281-338`.
- The random-key representation and the decoder, `:339-381` with
  `src/ehgat/environment/decoder.py`. Know the $4N$ chromosome layout, since it is also the
  XGBoost baseline's feature vector.
- The heterogeneous graph, `:382-403` with `src/ehgat/surrogate/graph.py`. Which quantities
  sit on nodes and which on arcs, and why that forces edge conditioning.
- E-HGATv2 itself, `:404-532` with `src/ehgat/surrogate/ehgatv2.py`.
- Attribution-guided search, `:831-892` with `src/ehgat/search/tape_guidance.py`. Follow one
  gradient through to the mutation probability and the operator choice.

### Day 5 — The coupled regime (5 h)

`paper/main.tex:214-261`, then `src/ehgat/explain/fused_ehgat.py:57-110` for the contention
features and the unrolled forward, and `tests/unit/test_power_evaluator.py` for the five
properties that are actually asserted — in particular that a large budget reduces the
coupled evaluator to the uncoupled one. This is the regime where the network learns
something with no closed form, so it is the strongest ground for the method; it is also
your own extension rather than his, and both halves of that need saying.

### Day 6 — The remaining results and the limitations (7 h)

The subsections not yet covered: faithfulness at `:996`, granularity at `:1019`, fidelity at
`:1092` with `tab:fidelity`, the landscape analysis at `:1239` with `tab:critpath_summary`,
the cost of the faithful signal at `:1751`, and coupled fidelity at `:2247`. Then
`:2268-2292`, the discussion and limitations, which is the section to know best of all —
volunteering a limitation before it is found is worth more than any result.

Read `PAPER_FINDINGS.md` selectively for the claims it records as unsupported, and
`docs/PROGRESS.md` for what is marked NOT RUN.

### Day 7 — The demonstration (6 h)

Most of this already exists. `scripts/run_critical_path_demo.py` was written for exactly
this purpose — its docstring records that it produces "the human-readable worked example the
advisor asked for" — and it already traverses the exact critical path, prints the additive
decomposition

    C_max = sum of on-path leg durations + sum of on-path QC handlings,

and then shows the fused TAPE recovering the identical path with per-activity errors. Run it
first and read its output line by line; that is items 1 to 4 below already built.

What to assemble into one notebook against a small instance, run enough times to trust:

1. Load L01, decode a chromosome, show the schedule.
2. Evaluate exactly; show $C_{\max}$ and $E$.
3. Show the critical path and its additive decomposition.
4. Show the fused model's predicted path beside it — the faithfulness claim in one cell.
5. Show the gradient becoming a mutation probability, and the move the guidance selects.
6. One front, with the guided and unguided arms side by side.

Items 5 and 6 are the additions. Do not demonstrate anything live from a terminal; a failed
import costs more than the demonstration gains.

Then rehearse against the question list below, aloud, twice.

---

## The questions to be able to answer cold

1. Why is the makespan a longest path, and what follows from that?
2. What does the network learn, and what does the architecture compute?
3. Why is embedding the recurrence not building in the answer?
4. Why not XGBoost and TreeSHAP, as in your XAI and MOO plan?
5. Is the explanation read off the surrogate, and if so how is that different from TreeSHAP
   on XGBoost?
6. In the uncoupled problem the leg times are closed-form — so what is the network for?
7. Does your mp-BRKGA match mine, and at what budget?
8. Where does the optimisation advantage come from, and is it screening or attribution?
9. What holds as $N$ grows, and on whose instances?
10. In what sense does the surrogate learn the Pareto front behaviour?
11. Why is there a power constraint in a container terminal paper?
12. What in this report do you not yet believe?

Question 6 and question 12 are the two that decide how the meeting goes. Question 6 has a
real answer — the coupled power-wait, and amortisation across a search — but it must be
given without defensiveness. Question 12 should be answered from the limitations section
directly, and answered first rather than last.

---

## Notes on method

**Work the hand example before opening any model code.** The code then reads as an
implementation of something already understood, rather than as several thousand lines to
be memorised.

**Roughly 4,000 of the 9,800 lines are load-bearing for a defence.**
`src/ehgat/search/attention_nsga2.py` and the benchmark harnesses can be treated as
plumbing unless he asks about the search loop specifically.

**Anything not yet run should be described as not yet run.** The record already carries the
corrections; matching that register in person costs nothing and is the thing he asked to
confirm.
