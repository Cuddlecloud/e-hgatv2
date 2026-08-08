# Draft email to Prof. Homayouni

> Working draft. Lives in the working repository only. It is not in the review tree the
> advisor reads, and must not be copied into it.

---

**Subject:** Thesis progress, codebase for review, and a request for the DS/DL instance data

Dear Dr. Homayouni,

I am sorry this has taken so long to reach you. You told me to take my time with the papers,
and I did, but I then spent much longer than I expected on the experimental side: I went
through several architectures before one of them held up, and the runs were slow enough that
each attempt cost days on a rented machine. For a good while I could not have told you
whether the approach would work, so I kept waiting for something worth sending. I should
have written to you mid-way with the uncertainty included instead of going quiet.

The method is settled now and the results are stable, so I would like to share the code and
the write-up, and to ask for some instance data I need for the final experiments.

Repository: https://github.com/aayushjha1729/e-hgatv2 — the README gives the reading order
and how each reported number is regenerated.

## How it follows the three directions

The work stayed on the track you set: knowledge gathered during the search is fed back into
the search. Concretely, a surrogate-assisted NSGA-II produces `k·λ` offspring per generation,
ranks them with a learned surrogate of `(C_max, E)`, and passes only the best `λ` to the
exact evaluator. The exact-evaluation budget per generation is therefore unchanged, so every
comparison is made at matched exact evaluations. The same screening sits inside mp-BRKGA
(`run_mp_brkga(..., screen_fn=...)`), which lets the surrogate be switched on and off within
one algorithm rather than compared across two. That is direction 3.

What makes directions 1 and 2 work is where the makespan comes from. The network does not
regress it. It predicts the individual leg durations and handling delays, and those are
composed through the exact max-plus critical-path recurrence. The composition is exact by
construction, so the model's gradient with respect to each leg is exactly the binary
critical-path indicator — the surrogate hands back, for free and exactly, which task orders
and speed choices are binding. That is the feature-importance and landscape analysis of
direction 2, and aggregating the same quantity across the front, weighted by the local
trade-off between `C_max` and `E`, is what lets the model describe the Pareto front's
behaviour rather than only its location. The surrogate is a graph network over the schedule
rather than a feature vector, so a model fitted on small instances applies unchanged to large
ones; a tabular surrogate fitted at `N=10` cannot be evaluated at `N=160` at all.

The physics is your published model, verified rather than assumed: Eqs (2)–(4) and (10)–(18)
evaluated forward with the binaries fixed by the decoded schedule. It agrees to zero
discrepancy with a line-by-line transcription solved by fixed-point iteration and with
exhaustive enumeration of all `3^(2N)` speed assignments on small instances. Eqs (5)–(9) and
(19) hold by construction through the random-key decoder, following §4.2 of the 2022 paper.

## The peak-power-coupled regime, with its limits

I also built a peak-power-coupled version, following the model in your ITOR 2025 paper with
the budget over the AGV travel legs rather than machines: a fleet-wide instantaneous budget
of 30 kW, above the largest single-leg draw of 19.8 kW, so concurrent legs contend and a leg
may have to wait for budget to free. The makespan then has no closed form: it is
resolved by a deterministic event-driven simulator, and the binding path is set partly by
disjunctive power-wait arcs. That is the setting where the bottleneck cannot be read off the
schedule by inspection, and where the surrogate earns its place.

It is also the weakest part of the results, and I would rather state that plainly than let
it look settled. Held-out `R²` falls from ≈0.99 to ≈0.80, critical-path recovery to 0.85 at
`N=20`, and size transfer holds only to about `N=25`, where the uncoupled model holds out to
very large `N`. The makespan-optimal extreme of the coupled `N=10` front collapses outright
— the maximum-contention corner, where every vehicle runs at top speed and the binding path
is dominated by the power-wait arcs that have no closed form. A deeper unroll and a larger
sample gave the identical number, so it is an accuracy ceiling rather than a sampling
artefact.

I suspect the gap is partly that I am training against instances I generated myself. Your
ITOR paper states the model for job-shop machines, so I had to decide how the budget applies
to AGV travel legs, what value it takes, and how contention is arbitrated — I currently use
a fixed dispatch priority rather than treating the arbitration as a decision. If you have
the peak-power instances from that work, or would tell me which of those choices matches
what you had in mind, I could put the coupled results on the same footing as the uncoupled
ones instead of reporting them as the weaker half.

## What I need

The results rest on the Table 5 loading instances plus synthetic dual-cycling instances
generated from your Table 4 distance matrix. Five things would close the gaps:

1. **Your published per-instance `C_max` and `E` values.** I have re-implemented mp-BRKGA
   from the published description and it is my main comparison, but I have not been able to
   validate it against your reported numbers, so the write-up has to describe it as a
   re-implementation rather than as your algorithm. Even a subset of instances would let me
   state the agreement quantitatively. This is the one I would value most.
2. **The peak-power instances and budget values from the ITOR 2025 paper**, together with
   whatever you can tell me about how the budget should carry over to AGV travel legs. This
   is what would let the coupled regime rest on your data rather than on my reading of the
   model, and it is where the results are weakest.
3. **The DS instance task lists (dual-cycling)**, which is presently demonstrated only on my
   synthetic instances.
4. **An extended QC↔LU distance matrix.** Table 4 spans QC1–QC6 and LU1–LU6; the larger DL
   instances have 8–16 cranes and exceed it.
5. **The DL instance task lists**, once that geometry is available.

On the discrete-event simulation model from your former student: I have set it aside for now,
because the attribution needs a deterministic evaluator and stochastic service times would
remove the exactness the whole analysis rests on. It would be a natural validation asset
later, and I would be glad to discuss where it fits.

## Where I would like your direction

Before I run anything further I would rather have your view than guess, on four points.

1. **The architecture.** The surrogate as it stands is a heterogeneous graph attention
   network with the max-plus critical-path layer composed on top. Is that the form you want
   this to take, or would you prefer I change it — a different surrogate, or the XGBoost and
   TreeSHAP pipeline of the XAI paper, which I currently keep as the baseline it is compared
   against.
2. **Evaluation and metrics.** I report hypervolume and IGD+ against a reference front, with
   Friedman and Holm-corrected Wilcoxon tests across seeds, and critical-path recovery for
   the explanation. Are those the comparisons you would want to see, and is there a metric
   you consider standard here that I have left out.
3. **Instance sets.** Results are on the Table 5 loading instances and on dual-cycling
   instances I generate from your Table 4 distances. Which sets would you want the claims
   made on, and at what sizes.
4. **How far to generalise.** The findings currently hold on instances up to a few hundred
   tasks in the uncoupled regime and near the training size in the coupled one. I would like
   to know whether you want them pushed to larger instances and to the coupled regime, or
   whether it is better to state them narrowly on the sizes where they are solid.

I would also be grateful for any comments on the formulation, particularly on whether the
baseline configurations are the ones you would consider fair.

Thank you for your patience with the delay.

Kind regards,
Aayush

---

## Notes on this draft (for you, not the email)

- **This file is in the working repository, not the review one.** Absent from the public
  review repo. Do not copy it into the review tree.
- **Aligned to his own correspondence.** He writes "Dr. Mahdi Homayouni" and signs "Kind
  regards", so the salutation and sign-off match. He framed the work as three numbered
  directions and told you to keep it "in the same track (guiding the optimization algorithm)
  using knowledge/explanation/pattern gathered during the search", and separately asked that
  the surrogate learn the **Pareto front behaviour**. The method section now answers those in
  his vocabulary and names directions 2 and 3 explicitly, rather than presenting the method
  on its own terms. His DES mention is attributed to his former student, as he put it.
- **The apology gives a reason and does not grovel.** One paragraph, three concrete causes,
  one admission. It also picks up his own "take your time" so the delay reads as over-applied
  advice rather than neglect. Do not extend it — a longer apology reads as anxiety, and the
  rest of the email is the actual answer to it.
- **The mp-BRKGA data request leads the list.** It is the pivotal ask and the one that most
  affects how strongly you can state the results. It stays framed as his algorithm needing to
  be represented correctly, not as a baseline you beat. Do not send a version claiming to
  beat mp-BRKGA `11/11` without that caveat: the mp-BRKGA in question is your own
  re-implementation, and asserting a win over his algorithm using your copy of it, in the
  message where you ask for his data, is the one avoidable misstep here.
- **The coupled section is deliberately self-critical.** He will read "no closed form" as the
  interesting part and "R² 0.80" as the weak part; stating both yourself is stronger than
  having him find the second. The closing question on power arbitration gives him something
  concrete to advise on.
- **No "as we discussed" on the peak-power regime.** `refs/advisor_papers_notes.md` records
  that peak-power coupling is his own published direction (ITOR 2025, ref [1] of his XAI+MOO
  paper), and it is likely he raised it in a meeting — but that is not confirmed, so the
  draft says only "following the model in your ITOR 2025 paper". Claiming a shared memory he
  may not have is the kind of small error that costs credibility; citing his paper carries
  the same signal with no risk. If you are certain he asked for it, add it back.
- **The four direction questions are the actual ask of the email.** He warned against being
  too ambitious and asked for a one-page proposal; you are sending a full paper. Asking him
  to choose the architecture, the metrics, the instance sets and how far to generalise
  restores his control over scope, which is what the warning was about. It also converts the
  coupled-regime weakness from a confession into a question he can answer.
- **He asked for a one-page proposal and warned against being too ambitious.** You have
  delivered a full paper instead. That is fine, but do not draw attention to the mismatch —
  the email answers his directions in order, which is the substance of what he wanted.
- **The paper is ML-framed and the email is not.** If you send `main.tex` as-is, expect the
  abstract to read as interpretability-first; consider saying in the covering line that the
  write-up targets an ML venue and that Sections 5–7 are the optimisation results.
- **Deliberately omitted:** hypervolume/IGD+ definitions, Friedman/Nemenyi machinery, R²
  curves, the guidance ablation. They belong in the paper, not the first email. The metrics
  are now *named* in direction question 2, which is different from explaining them.
- **Fill in before sending:** whether to name a target venue.
- **The repository is public.** Anyone with the URL can read it, including the manuscript
  PDF. Consider whether you want it public before submission, or private with him invited.
