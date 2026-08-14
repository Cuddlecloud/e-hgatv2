# Draft email to Prof. Homayouni

> Working draft. Lives in the working repository only. It is not in the review tree the
> advisor reads, and must not be copied into it.

---

**Subject:** Thesis progress, code and paper for review, and a data request

Dear Dr. Homayouni,

I am sorry for the long silence. Most of it went on the experimental side, and I went through
several designs that did not survive contact with the data, so for a long stretch I could not
have told you whether the approach would hold. It has settled now. The paper is attached, and
the code is at https://github.com/aayushjha1729/e-hgatv2 — the README gives a reading order and
says how each reported number is regenerated.

I would like to walk you through how I got here rather than only the results, because the route
is what my questions at the end are about.

I started with the pipeline in the XAI+MOO plan, a tabular surrogate with TreeSHAP on top. It
fits the objective, but I got stuck on validation. TreeSHAP attributes to the surrogate's own
function, so if that function is wrong about the scheduling structure the attribution is
confidently wrong along with it, and I had nothing to check it against. I built it anyway and
kept it as the comparison. On the small instances the flat surrogate reaches an out-of-sample
R² of about 0.12 on makespan, and its importance profile moves roughly 43% of the mass off the
assignment and sequencing decisions and onto the speed settings, where a variance decomposition
on the exact evaluator puts almost none.

What changed the approach was noticing something about your model that I should have seen
earlier. Once a solution fixes the AGV assignments, the sequences and the speeds, the
disjunctive constraints are resolved, and what remains is an acyclic precedence graph with one
chain per vehicle and one per crane. Every completion time in Eqs. (10)–(18) is then a maximum
of sums along those chains, so the makespan is a longest path — the same reduction as the
disjunctive graph in job shop. On that graph, the classical forward earliest-start pass and the
backward trace of binding predecessors return the critical activities, and the float on every
other one, exactly.

I want to be direct that this is the critical path method and that I am not presenting it as
new. Given the durations of a solution the evaluator has already run, it is exact, it costs
almost nothing, and no learned model improves on it. What I think is worth something is what it
makes available.

For your second direction it gives precisely the relationship you described. The partition is
into activities that bind and activities that carry float, and float is the operationally
meaningful quantity: a leg with float is a leg whose AGV can be slowed to save energy at no cost
in makespan, which is the mechanism that puts a solution on the front. Aggregating over sampled
solutions and grouping by decision type — which AGV, position in that AGV's sequence, loaded
speed, empty speed — produces the landscape you asked for, and because the attribution is exact
it can be checked rather than argued for. Separately, comparing the non-dominated set against
dominated solutions, the descriptor that separates them is AGV load balance: the Pareto
solutions are the balanced ones. Sobol indices reach a similar ranking, but they need several
thousand exact evaluations at ten tasks and give one number per family for the whole population
rather than per solution.

The network is not doing that work, and I do not think it should. Where it earns its place is
elsewhere.

For the third direction the surrogate sits inside NSGA-II. Each generation produces more
offspring than it needs, the network ranks them, and only the best fraction goes to the exact
evaluator, so the exact-evaluation budget per generation is unchanged and every comparison is at
matched budget. The attribution then chooses where to mutate: it identifies the currently
binding task, and whether that task is held up by its vehicle or by its crane, which selects
between reassignment, a sequence swap, and crane reordering. Against random NSGA-II and
single-population BRKGA the guided version wins at every problem size I tested, and the margin
grows steadily with size. Against your multi-population variant it wins at every size except one,
where the two are level. At the largest sizes the classical baselines have effectively not
converged inside the same budget while the guided search still recovers most of the reference
front.

The part I would most like your reaction to is size transfer. Because the network predicts
per-leg durations rather than a schedule-level objective, the same fitted model applies
unchanged to instances far larger than the ones it was trained on. I train once at sixteen tasks
and the makespan fit stays above 0.98 out to several thousand tasks, while an otherwise
identical model with a pooled global read-out degrades to worse than predicting the mean. A
tabular surrogate cannot be used this way at all, because its input width is fixed at training
size. If the aim is to carry knowledge from small solved instances to large unsolved ones, that
seems to me the property that matters.

On the point in your second email about the surrogate learning the front's behaviour: running
the attribution at each point of an approximated front and weighting it by the local
makespan–energy trade-off gives a compact description of what binds where. The two ends differ
sharply. At the makespan end almost all binding activity is AGV travel. At the energy end the
vehicles have slowed, and on some instances the cranes serialise behind them and enter the
critical path — though not on all of them, so I report it as an instance-level property rather
than a rule. A small predictor taking only fleet and crane counts then places a new instance on
that axis without running the search.

Three things are weak, and I would rather flag them than have you find them.

The mp-BRKGA comparison is against my own re-implementation from the description in the 2022
paper. With nothing published to calibrate against, everything I say about beating it is a
statement about my re-implementation. That is the request I care most about below.

I also built a peak-power-coupled variant after you raised it, in which a fleet-wide
instantaneous budget couples the vehicles. Three modelling choices in it are mine rather than
yours — how the budget applies to travel legs rather than to machines, its value, and how
contention is resolved when two vehicles demand power at once — so I have kept it as an
exploratory section rather than as a test of your formulation. I would rather settle the
uncoupled problem properly first, but I am happy to take it further if you would like.

The published loading instances turn out to be transport-bound almost uniformly, so they cannot
discriminate between a predictor of front composition and a constant. I had to build a set with
varying fleet-to-crane ratios to test that at all, and I report the saturation as a property of
those instances.

What would help, roughly in order:

1. The per-instance C_max and E values from your mp-BRKGA runs. Even a handful of instances
   would turn a re-implementation into a calibrated baseline.
2. The DS dual-cycling task lists. I am currently working from the Table 5 loading instances of
   the book chapter, plus synthetic dual-cycling instances built on the Table 4 distances.
3. An extended QC↔LU distance matrix. Table 4 covers QC1–6 and LU1–6, and the DL instances have
   8 to 16 cranes.
4. The DL task lists, once that geometry exists.

I looked for the terminal instances on the page linked from the 2022 paper, but it carries only
the job-shop sets.

Three things I would like your view on. First, is this the direction you want, or would you
rather I return to the XGBoost and TreeSHAP pipeline from the plan? I have kept it as the
baseline everything is measured against, but I do not want to have moved away from your design
without your agreement. Second, to validate the importance rankings properly I intend to delay
one activity by a fixed amount on the exact evaluator and score each method against the realised
change in makespan — the attribution, the classical float ranking, TreeSHAP and Sobol on one
common measure. Is that the comparison you would want, and is there a reporting standard beyond
hypervolume, IGD+ and Friedman with Holm-corrected Wilcoxon that I should be using? Third, would
you rather I push toward larger instances, or keep the claims narrow where they are solid?

I have set the discrete-event simulator aside for now, since the attribution needs a
deterministic evaluator, but it looks like the right tool for validating the coupled variant
later.

Kind regards,
Aayush
