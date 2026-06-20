# CANONICAL CONTEXT — READ THIS FIRST (anti-amnesia doc)

> Purpose: every fresh agent/session keeps re-deriving (and getting wrong) the same
> few facts about *what this project is for* and *why the GNN is justified*, wasting the
> author's time and money. This file is the settled ground truth. **Do not relitigate the
> conclusions below from scratch. If you think one is wrong, say so explicitly and cite
> evidence — do not silently revert to a previously-debunked framing.**
>
> Last settled: 2026-06-20.

---

## 0. TL;DR (the one paragraph a new model must absorb)

(NOTE: whether the target is the **uncoupled** or **peak-power-coupled** problem is an OPEN
question — see §1. If coupled, the surrogate gains a second justification: coupled evaluation
has no closed form, so the GNN is *needed* for evaluation too. The headline below holds
either way.)

The GNN's consequential contribution is **NOT** predicting/evaluating the *uncoupled*
objective (it's exact and cheap — O(N) — so a surrogate adds nothing there). The
GNN's contribution is **guiding the NSGA-II search so multi-objective optimization scales**:
attention-guided search converges faster and to a better Pareto front than bare NSGA-II,
and that advantage is expected to **grow with instance size N**. This is the SCALE
argument, it lives on the **optimization axis** (the factorial, hard part), and it is the
paper's headline (Requirement 3 / the advisor's "ultimate goal"). It survives a NeurIPS
reviewer because steering a factorial search is something no cheap exact routine can do.

---

## 1. What the advisor actually wants (settled)

Source: advisor email (2026-05-30) + three attachments + `refs/advisor_papers_notes.md`.

- **Problem = the CONTAINER TERMINAL problem**, not Job Shop. Job Shop (EEJSP) is only the
  example domain in the *methodology template* paper (Paper C, Homayouni & Davari
  "Explainable AI-Guided NSGA-II"). The actual problem is joint QC + speed-adjustable AGV
  (SA-AGV) dual-cycling scheduling, bi-objective **min (C_max, Energy)** — defined by
  Papers A (FSMJ 2023) and B (Book Chapter 2022).
- **COUPLED vs UNCOUPLED is an OPEN QUESTION — confirm with the advisor before committing.**
  Do NOT assert this is settled (an earlier session wrongly did). Evidence cuts both ways:
  - *Uncoupled:* Papers A & B (the "understand the problem" papers) have no peak-power
    constraint.
  - *Coupled / peak-power:* **Requirement 3 explicitly ties to the Homayouni_XAI+MOO paper
    (Paper C)**, which is on JSP and whose **reference [1] is the peak-power JSP paper
    (Homayouni & Fontes 2025)**. The XAI method (TreeSHAP/feedback) is described **only in
    the JSP/peak-power setting, never on the container problem.** So the advisor may well
    want the **peak-power-coupled** version.
  - **Resolution = ask him directly** (uncoupled container vs peak-power-coupled; container
    domain vs JSP). The repo already supports the coupled path (power simulator, fused TAPE
    wait head, coupled faithfulness at pp30), so neither answer is blocked.
- **Domain:** likely the **container terminal** (Requirement 2 names AGV task order, AGV
  speed, crane workload — container entities, not JSP machines/operations; the ex-student's
  sim is a container terminal). But the advisor referenced the JSP-based XAI+MOO plan for the
  method, so confirm domain too.
- **The method = the XAI+MOO pipeline (Paper C)**, decomposed into three requirements:
  1. **Req 1 — Feature engineering** from post-hoc analysis (XAI / causal-ML).
  2. **Req 2 — Landscape / feature-importance analysis** on small instances explaining why
     solutions are Pareto-(near)optimal (relationship between input vars — AGV task order,
     AGV speed, crane workload — and objectives).
  3. **Req 3 — Feedback algorithm** that steers the optimizer's search. **This is the
     advisor's stated ultimate goal and our strongest result.**
- Paper C's *own proposed method* is XGBoost surrogate + TreeSHAP + clustering + local
  search. **Our pitch surpasses it** with a faithful GNN+TAPE explainer. Keep TreeSHAP/
  XGBoost as the documented baseline/foil (Claim 3), not a strawman.

---

## 2. The evaluation-vs-optimization distinction (settled — do NOT conflate)

Two different "exact" operations get confused every session:

| Operation | What it does | Cost | Scales to N≥100? | Who does it |
|---|---|---|---|---|
| Exact **evaluation**, uncoupled | score one given schedule (C_max,E) | O(N), cheap | yes | `evaluator.py` (max-plus longest path) |
| Exact **evaluation**, coupled | score one schedule under peak-power | expensive, no closed form | poorly | power simulator |
| Exact **optimization** (MILP) | find optimal / true Pareto front | factorial/exponential | NO (dead ≥40 tasks) | Gurobi |
| **Search** good schedules | many cheap evals | yes | **NSGA-II** (not the GNN) |
| GNN surrogate/explainer | predict + attribute | O(L·N·d) | yes, but no win vs uncoupled exact eval | the GNN |

Consequences (do not re-derive incorrectly):
- "MILP can't scale" justifies using a **metaheuristic (NSGA-II)**, NOT the GNN-as-solver.
- Evaluating a schedule you hold is cheap; *searching* the factorial space is the hard part.

---

## 3. Why the GNN is justified (settled) — and what NOT to claim

**The GNN earns its place via (in order of strength):**
1. **Search guidance / scale (Req 3, HEADLINE).** Attention-guided NSGA-II converges
   faster and to a better front than bare NSGA-II; the advantage grows with N. This is the
   scale argument and the optimization-axis win. See §4.
2. **Coupled regime.** Peak-power evaluation has no closed form → a surrogate is *necessary*
   (the only place the surrogate is required, not merely nicer).
3. **Faithful, scalable explanation vs textbook XAI** (Sobol / TreeSHAP). Measurable
   faithfulness + scaling win. Much of this win comes from using critical-path structure
   (which the exact oracle also has) — the GNN inherits it and adds amortization.
4. **Amortized generalization.** Trained once → faithful attributions on unseen/larger
   instances in one pass, no simulator in the loop.

**⚠️ DO NOT re-scope "GNN-necessity" to the coupled regime only.** A recurring mistake
(made again 2026-06-20) is saying "the GNN is only necessary in the power-coupled regime."
That is true for the **evaluation axis ONLY**. The GNN earns its place on **four** axes, and
**three of them apply to the closed-form / uncoupled problem too**:

| Axis | Needed on closed-form (uncoupled)? | Why |
|---|---|---|
| **Optimization / search scaling** (HEADLINE, Req 3) | **Yes** | Attention-guided NSGA-II converges faster + to a better front than random NSGA-II and BRKGA — non-overlapping 95% CIs (`n10_screen`). Closed-form *evaluation* is cheap, but the factorial *search* is not, and the GNN steers it. |
| **Generalization (amortization)** | **Yes** | Train once → faithful guidance/attributions on unseen/larger instances in one pass, no simulator in the loop. |
| **Faithful landscape / explanation** (Req 2) | **Yes** | TAPE gives per-schedule critical-path attributions, validated vs the exact oracle at small N, scalable beyond it. |
| **Evaluation** | **No — coupled-only** | Uncoupled eval = O(N) longest path, cheap → GNN redundant *for evaluation*. Only peak-power coupling makes evaluation expensive/open-form → GNN necessary there. |

So the correct one-liner: **the GNN's *evaluation-necessity* lives entirely in the
power-coupled regime, but its headline value (scaling optimization) plus generalization and
faithful-explanation value apply to closed-form uncoupled problems too.** The
optimization-scaling axis is the *primary* justification — and it is exactly the
closed-form-applicable one, not a coupling artifact.

**NEVER claim these (a reviewer will kill the paper):**
- ❌ GNN is *faster* than exact for uncoupled single-schedule evaluation. (Same O(N), worse
  constant. False.)
- ❌ GNN is *more accurate* than the exact oracle on uncoupled. (Exact is the ground-truth
  ceiling; the GNN approximates it. Use exact as the *validation* reference, not a thing to
  beat.)
- ❌ "We use a GNN because the uncoupled problem doesn't scale." (Uncoupled *evaluation* is
  O(N) and scales fine; only *optimization* is hard, and NSGA-II handles that.)

**The validation framing (use this):** the uncoupled problem is cheap *on purpose* — it
gives exact ground truth to *validate* that the learned explanations/search-guidance are
faithful, which licenses trusting them where exact is infeasible (coupled / large N).

---

## 4. Headline empirical result (settled) + the decisive experiment

**Current model = `experiments/n10_screen/` (surrogate screening + attention-guided search).**
N=10, 30 seeds, pop=200, gen=100. Golden (oracle PF*) HV = 1,212,410.

| Method | Final HV (mean) | 95% CI | IGD+ |
|---|---|---|---|
| **E-HGATv2-NSGA-II (ours)** | **1,131,307** | [1,120,042, 1,142,373] | **36.96** |
| NSGA-II (random) | 1,073,420 | [1,053,166, 1,092,197] | 71.27 |
| BRKGA (advisor's method) | 1,055,694 | [1,038,292, 1,072,199] | 81.80 |

- **Statistically significant**: ours' HV lower bound (1,120,042) > random's upper bound
  (1,092,197) → non-overlapping 95% bootstrap CIs. Same on IGD+.
- Convergence chart `experiments/n10_screen/hypervolume_convergence.png` shows ours (green)
  separating from random/BRKGA ~gen 5 and dominating through gen 100 (~2.5× fewer
  generations to reach the same HV).
- Beats **BRKGA** too — the advisor's own 2023 metaheuristic.

**⚠️ Data-hygiene warning:** the `faithfulness` block in `n10_screen/benchmark_results.json`
(`precision_at_1 = 0.6167`, `spearman_rho = -0.00745`) is **byte-identical to the old
`n10_live` run** — it is STALE/copied, not regenerated for this model. Do NOT cite it.
Regenerate faithfulness with the current model. (Faithfulness is a separate axis anyway; the
fused TAPE model is the faithful one — see §6.)

**THE decisive experiment (still TODO):** run the **current** screening model at
N = 5, 10, 20, 50, 100 (same 30-seed protocol) and plot **(HV_ours − HV_random) vs N**.
If the gap is ≤0 at small N and grows monotonically with N, the scale claim is made
empirical: "the GNN's search advantage emerges and strengthens with problem size." This
single figure is the most valuable remaining result.
- NOTE: the old N=5 "random wins" result was a *previous mechanism* (pre-screening), so it
  is NOT comparable to the current model. The whole gap-vs-N curve must use the current
  model.

---

## 4A. Concrete ways GNN+TAPE is effective (capabilities + evidence)

Each item = capability, the mechanism, the hard evidence we have, and the honest caveat.
**Keep the two signals separate:** *attention* (search guidance, NOT faithful) vs *TAPE*
(faithful explanation). Do not claim attention is faithful (see §3).

1. **Faithful explanation by construction (TAPE).**
   - Mechanism: makespan flows through a differentiable max-plus DP, so `dC_max/d(leg)` is
     the exact binary critical path — no Jacobian smearing.
   - Evidence (fused model vs exact oracle, **coupled pp30**, N=10/20/50, 20 seeds):
     **arc critical Jaccard = 1.000 (perfect)**, **leg critical Jaccard ≈ 0.91–0.93**.
   - Caveat: measured coupled only so far; uncoupled faithfulness run still TODO. Faithful
     signal = TAPE, NOT attention.

2. **Search guidance that scales MOO optimization (the headline).**
   - Mechanism: GNN attention steers NSGA-II task/operator selection.
   - Evidence (`n10_screen`, **uncoupled container**, N=10, 30 seeds): final HV
     **1,131,307** vs random NSGA-II **1,073,420** vs BRKGA **1,055,694** (golden 1,212,410);
     IGD+ **36.96** vs 71.27 vs 81.80; **non-overlapping 95% CIs** (significant); converges
     to a given HV in ~**2.5× fewer generations**; **beats BRKGA (the advisor's own method)**.
   - Caveat: this win currently rides on the **bare attention (unfaithful)** signal, not
     TAPE. Best paper move = make TAPE drive the guidance so "faithful explanations guide
     search" is one evidenced claim. Scaling-vs-N curve still TODO.

3. **Scalable landscape / feature importance (Req 2), GNN/TAPE not Sobol.**
   - Mechanism: aggregate per-schedule TAPE subgradients into decision-family importance +
     Pareto contrast (`src/ehgat/explain/gnn_landscape.py`); one fwd/bwd per schedule,
     batchable.
   - Evidence: cost is flat per schedule vs Sobol's `samples × families` exact-evaluator
     blowup; validated against the exact oracle via rank agreement at small N.
   - Caveat: the headline large-N landscape numbers still need a run.

4. **Exact additive energy + physics-anchored makespan calibration.**
   - Evidence (coupled pp30): **R² energy = 1.000** (additive head is exact); **R² makespan
     ≈ 0.78–0.80**; TAPE makespan abs-error ≈ 40 s (N=10) → ≈ 101 s (N=50).
   - Caveat: R² makespan ~0.8 is good, not perfect — report honestly.

5. **Handles the coupled regime where there is NO closed form.**
   - Mechanism: the GNN learns the per-leg power-wait (a contention fixed point with no
     analytic formula) via the physics-unrolled wait head.
   - Evidence: faithfulness holds under coupling (item 1's pp30 numbers). This is the one
     regime where the surrogate is *necessary*, not merely better.

6. **Amortized generalization (the NCO value).**
   - Mechanism: train once → faithful attributions on unseen/larger instances in one forward
     pass, no simulator in the loop.
   - Caveat: conceptual/architectural so far — a held-out-instance generalization experiment
     is not yet run. Do not claim it as measured until it is.

## 4B. Why the baselines lose (explicit) — XGBoost+TreeSHAP and Sobol

These are the head-to-head reasons GNN+TAPE beats the two baselines (the advisor's own
proposed method is XGBoost+TreeSHAP, Paper C — keep it as the documented foil, not a
strawman). All three failure modes below are structural, not tunable.

**XGBoost + TreeSHAP loses because:**
1. **Feature extraction.** XGBoost is **structure-blind** → it requires manual feature
   extraction/engineering from the schedule. The **GNN consumes the schedule directly as a
   graph and learns its own representation**, which **renders the feature-engineering step
   unnecessary.** (So Req 1's "feature engineering" is an artifact of the *tabular tooling*,
   obviated by the graph model — not a property of the problem.)
2. **Cannot encode cascading temporal delays.** Being tabular/additive, TreeSHAP cannot
   represent "task *j* matters *because* it gates *k* on the critical path." The cascade is a
   topological/temporal relationship a flattened feature table cannot express.
3. **Unfaithful.** It sits on a flattened surrogate (~R² 0.5), so it explains a half-wrong
   function. (Contrast: fused TAPE arc Jaccard = 1.0 vs ground truth.)

**Sobol loses because:**
1. **Cannot encode cascading temporal delays either.** Sobol gives **aggregate variance
   shares per family** (population level) — not per-solution critical-path structure. It
   cannot say which specific task gates which downstream task.
2. **Coarser granularity.** TAPE is **per-schedule / per-task / per-edge**; Sobol is one
   aggregate number per family. So **GNN+TAPE provides a strictly more granular landscape**
   than Sobol.
3. **Doesn't scale and doesn't invoke the model.** Sobol costs `samples × families`
   exact-evaluator calls (blows up with N), and it bypasses the GNN/TAPE entirely — defeating
   the causal-ML/GNN thesis of the paper.

**Net: GNN+TAPE wins on (a) no feature extraction needed, (b) encodes the makespan cascade
via the exact critical path, (c) finer granularity than Sobol, (d) faithfulness (arc Jaccard
1.0), (e) O(N)/schedule scalability.**
- Honesty guards: the **cascade** claim is for the **makespan** objective (energy is additive,
  no cascade); the **large-N landscape** numbers are still TODO (validated vs oracle at small
  N only).

## 5. Data status (settled)

- **Only real published data wired in:** `data/distance_matrix.json` (Homayouni & Fontes
  2022, Table 4).
- **All instances are synthetic** via `build_toy_instance()` — there is **no DS/DL
  benchmark loader yet**. The DS/DL task sets exist only as text/screenshots in the PDFs.
- **Coupled (peak-power) has NO published benchmark anywhere** — it's the author's
  extension; labels come from the project's own simulator. This is a known credibility risk;
  defense = it's the novel regime with no closed form, validated against the exact simulator.
- **Highest-leverage data task:** write a DS/DL → `Instance` loader so the uncoupled
  validation + generalization runs on real published instances, and coupled instances
  inherit real geometry instead of round-robin toy assignment.

---

## 6. Architecture facts (settled, so they aren't re-litigated)

- **`FusedEHGATv2`** (`src/ehgat/explain/fused_ehgat.py`) = frozen EHGATv2 core + a
  **differentiable max-plus DP** makespan head + exact additive energy head.
  - The **GNN predicts the physical quantities** (leg times via `leg_head`, handling delay
    via `delay_head`, and in coupled mode the power-wait via `wait_head`). Default mode
    `use_physics_prior=False` = "GNN does the work." (`use_physics_prior=True` makes the GNN
    barely contribute — avoid for headline runs.)
  - The **max-plus DP is a deterministic differentiable *operator*** (like attention/softmax),
    not a closed-form solver. It composes the GNN's predicted quantities into C_max and makes
    `dC_max/d(leg)` the **exact binary critical path** → faithful by construction.
  - Honest framing = **physics-informed / differentiable-DP GNN**. The critical-path
    *structure* comes from the max-plus operator over GNN-predicted numbers, not "discovered"
    by the GNN. The GNN genuinely learns the **coupled power-wait** (no closed form) — the
    cleanest "the NN does real work" claim.
- **TAPE** = the gradients of the fused model (`fused_explainer.py`) OR of the exact oracle
  (`tape_explainer.py`, the small-N ground truth). Same `TapeExplanation` interface; the
  exact one validates the GNN one.
- **Req 2 landscape** = `src/ehgat/explain/gnn_landscape.py` (GNN/TAPE-derived, scalable),
  validated against the exact oracle via rank agreement at small N. The old Sobol-based
  `landscape.py` is kept only as a small-N cross-check / Claim-3 foil; the headline Req-2
  method is GNN/TAPE, NOT Sobol (Sobol doesn't scale and doesn't invoke the GNN/TAPE).

---

## 7. Anti-patterns that have wasted time before (do not repeat)

- Reading STALE experiment data (old `benchmark_results.json`, pre-screening N=5/N=10) and
  concluding the GNN loses to random NSGA-II. The CURRENT model is `n10_screen` and it WINS.
  Always confirm which model/mechanism produced a result before drawing conclusions.
- Re-proposing Sobol indices for Req 2. Settled: use GNN/TAPE; Sobol is a non-scalable foil.
- Framing the GNN as an evaluation/prediction surrogate for the uncoupled problem and then
  "discovering" it's pointless. Its value is **search guidance / scale**, coupled, and
  faithful explanation — not uncoupled evaluation.
- Conflating exact *evaluation* (cheap) with exact *optimization* (intractable). See §2.

---

## 8. Compute workflow (settled)

All compute runs on the RunPod L40S VM via `git push` / `git pull` (see
`.cursor/rules/compute-workflow.mdc`). Don't run heavy jobs locally.
