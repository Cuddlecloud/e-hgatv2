# Draft email to Prof. Homayouni

> Working draft. Kept outside the repository on purpose — this file is not in the tree the
> advisor will read, and must not be copied into it.

---

**Subject:** Thesis progress, codebase for review, and a request for the DS/DL instance data

Dear Prof. Homayouni,

I have reached the point where the method is complete and the results are stable, so I
would like to share the codebase and the current write-up for your review, and to ask for
some instance data I need for the final experiments.

**Repository:** *(link)* — the README lists where to start reading and how every reported
number is regenerated.

## What the method does

The optimisation loop is a surrogate-assisted NSGA-II. In each generation it produces
`k·λ` offspring instead of `λ`, ranks them with a learned surrogate that predicts
`(C_max, E)`, and passes only the best `λ` to the exact evaluator. The exact-evaluation
budget per generation is therefore identical to the unassisted algorithm — the surrogate
spends its own inference, not the evaluation budget — so all comparisons are made at
matched exact evaluations. The same mechanism is implemented inside mp-BRKGA
(`run_mp_brkga(..., screen_fn=...)`), which lets the surrogate be switched on and off
within one algorithm rather than compared across two.

Three design choices are worth flagging:

1. **The surrogate is a graph network over the schedule, not a feature vector.** This is
   what makes size transfer possible: a model fitted on small instances can be applied
   unchanged to larger ones, since it consumes the schedule graph rather than a
   fixed-length encoding. A tabular surrogate fitted at `N=10` cannot be evaluated at
   `N=160` at all. Training on small instances and evaluating on large ones is the central
   scalability claim.

2. **The makespan is computed by an exact max-plus longest path inside the model**, not by
   a regression head. The network predicts the individual leg durations and handling
   delays; those are then composed through the genuine critical-path recurrence. The
   composition is exact by construction, so prediction error enters only through the local
   durations, and the model's gradient with respect to each leg is exactly the binary
   critical-path indicator. This is the mechanism behind the feature-importance and
   front-behaviour analyses in directions 1 and 2 of your original note.

3. **The physics is the published model, verified rather than assumed.** The evaluator is
   the single-indexed MILP timing constraints Eqs (2)–(4) and (10)–(18) evaluated forward
   with the binaries fixed by the decoded schedule. It agrees to zero discrepancy with two
   independent implementations: a literal line-by-line transcription of the constraints
   solved by fixed-point longest-path iteration, and exhaustive enumeration of all `3^(2N)`
   speed assignments on small instances. The speed and power constants are taken from the
   2023 paper and are asserted against `v = α·v₀` at import. The assignment constraints
   Eqs (5)–(9) and (19) are satisfied by construction by the random-key decoder, following
   §4.2 of the 2022 paper, so they do not appear as explicit inequalities.

## The peak-power-coupled regime, and how far it actually got

I also built a second, harder regime and I want to report it with its limits rather than
only its successes. In it the fleet shares a single instantaneous power budget (I use
30 kW, above the largest single-leg draw of 19.8 kW), so concurrent travel legs contend and
a leg may have to wait for budget to free. The point of the construction is that the
makespan then has **no closed form**: it is resolved by a deterministic event-driven
simulator, and the binding path is set partly by disjunctive power-wait arcs. That is
exactly the setting where you cannot read the bottleneck off the schedule by inspection and
a differentiable surrogate has something to offer. I should be explicit that this
constraint is my own construction for stress-testing, is not part of your benchmark, and I
make no claim that it models a specific installation.

Three honest findings:

- **It works, but it is the weakest part of the results.** The surrogate's held-out `R²`
  falls from ≈0.99 (uncoupled) to ≈0.80, and the critical-path recovery averaged over the
  front drops to 0.87 at `N=20`. Both learned methods still beat all three non-learned
  baselines under coupling, but the margin is smaller and I report it as the weakest claim
  in the write-up.
- **There is a specific, understood failure at one end of the front.** On the coupled
  `N=10` instance the energy-optimal extreme is recovered exactly, while the
  makespan-optimal extreme collapses. That is the corner where every vehicle runs at
  maximum speed, contention is maximal, and the binding path is dominated by the very
  power-wait arcs that have no closed form. I re-ran it with a deeper physics unroll and a
  larger sample and got the identical number, so it is a genuine accuracy ceiling and not a
  sampling artefact.
- **It does not transfer across sizes.** The uncoupled model trained at `N=16` stays
  accurate out to very large `N`; the coupled one holds only to about `N=25` and then
  degrades. Coupled deployment would require training at or near the target size.

So the answer to whether the coupled regime is usable is: yes as a stress-test and for
most of the front, no as a size-transferable model, and not yet at the maximum-contention
extreme. If you think the power cap is worth pursuing as a realistic constraint rather than
a stress-test, I would value your view on how a terminal would actually arbitrate power,
because I currently resolve contention with a fixed dispatch priority rather than treating
the arbitration itself as a decision.

## What I need

The results currently rest on the Table 5 loading instances plus synthetic dual-cycling
instances I generate from your Table 4 distance matrix. Four things would let me close the
remaining gaps:

1. **The DS instance task lists (dual-cycling).** Dual cycling is presently demonstrated
   only on my synthetic instances. This is the item I would value most.

2. **Your published per-instance `C_max` and `E` values.** I have re-implemented mp-BRKGA
   from the published description and it is my main comparison, but I have not been able to
   validate it against your reported numbers. Until I can, I have to describe it in the
   paper as a faithful re-implementation rather than as your algorithm, which weakens
   comparisons that would otherwise be straightforward. Even a subset of instances would
   let me state the agreement quantitatively.

3. **An extended QC↔LU distance matrix.** The packaged Table 4 matrix spans QC1–QC6 and
   LU1–LU6. The larger DL instances have 8–16 cranes and exceed it, so I currently cannot
   run them on real geometry.

4. **The DL instance task lists**, once the geometry above is available.

If it is easier to send only part of this, item 2 is the one that most affects how strongly
I can state the results.

On the discrete-event simulation model you mentioned: I have left it aside for now, since
the attribution method requires a deterministic evaluator, and introducing stochastic
service times would remove the exactness the analysis depends on. It would be a natural
validation asset later.

I would be grateful for any comments on the formulation or the experimental design,
particularly on whether the baseline configurations are the ones you would consider fair.

Thank you,
Aayush

---

## Notes on this draft (for you, not the email)

- **This file lives outside the repository.** It is at `~/ADVISOR_EMAIL_DRAFT.md`, not in
  the release tree, so it cannot end up in the shared history. Do not move it back in.
- **Item 2 is the pivotal ask.** It is framed as your algorithm needing to be represented
  correctly, rather than as a baseline you beat. Do not send a version claiming to beat
  mp-BRKGA `11/11` without this caveat attached: the mp-BRKGA in question is your own
  re-implementation of his method, and asserting a win over his algorithm using your copy
  of it, in the same message where you ask for his data, is the one avoidable misstep here.
- **The coupled section is deliberately self-critical.** He is an OR researcher and will
  read "no closed form" as the interesting part and "R² 0.80" as the weak part; stating
  both yourself is stronger than having him find the second. The closing question about
  power arbitration also gives him something concrete to advise on, which is the cheapest
  way to get him invested.
- **The paper is ML-framed and the email is not.** The email leads with the optimisation
  loop, matched budgets and the MILP verification, then reaches the attribution mechanism
  as the *reason* the method works. If you send `main.tex` as-is, expect the abstract to
  read as interpretability-first; consider saying in the covering line that the write-up is
  targeted at an ML venue and that Sections 5–7 are the optimisation results.
- **Deliberately omitted:** hypervolume/IGD+ definitions, Friedman/Nemenyi machinery,
  R² curves, the guidance ablation. They belong in the paper, not the first email.
- **Fill in before sending:** the repository link, and whether you want to name a target
  venue.
