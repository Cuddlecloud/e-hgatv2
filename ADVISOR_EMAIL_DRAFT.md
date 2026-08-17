# Draft email to Prof. Homayouni

> Working draft. Lives in the working repository only. It is not in the review tree the
> advisor reads, and must not be copied into it.

---

Dear professor,

Apologies for the delay. I held off writing earlier because my work only recently reached a state that is defensible and much of the intervening time went on understanding the scheduling model well enough to design a surrogate around it while reading the surrounding ML literature; I spent the rest of the time on validation runs until the results were statistically sound. Please find attached the paper demonstrating the progress I have made so far.

Link to the public repo: https://github.com/aayushjha1729/e-hgatv2

**There are two components.**

- **E-HGATv2** is the surrogate, an edge-conditioned heterogeneous graph attention network. The schedule goes in as a graph where I have assumed tasks as the nodes, and the AGV precedences and the crane precedences are two separate kinds of arc, so the surrogate model sees the same structure the evaluator does. It predicts the individual travel and handling times, and a max-plus (longest-path) layer composes those into the completion times.

- **TAPE (Tropical Attributions for Physical Explanations)** is the attribution layer. It differentiates the surrogate's own makespan prediction back through the schedule and returns, for every travel leg and crane handling, its exact contribution — what is binding and what has float. Because it works on predicted durations it applies to a candidate before that candidate has been evaluated, which is what lets it select the neighbourhood the optimiser explores next — the feedback algorithm of your third direction.

**Against your three directions, and the front-behaviour point from your second email, in order.**

1. **Feature engineering.** The features are not hand-picked; they are the travel and handling quantities on the arcs, which is what the physics is written in. Because the model predicts one of those per leg instead of a single aggregate per schedule, it applies unchanged to instances much larger than the ones it was fitted on: fitted at N=16, the leg predictions hold at sizes two orders of magnitude beyond that, where a surrogate taking a fixed-length feature vector cannot be evaluated at all, its input width being fixed at the size it was trained on.

2. **Feature importance and landscape.** For a single solution, the analysis splits every leg and every crane handling into binding or having float. That is the operationally useful split, because a leg with float is one whose AGV can be slowed to save energy at no makespan cost, which is what puts a solution on the front in the first place. Doing this over many sampled solutions and grouping by decision type — which AGV a task goes to, where it sits in that AGV's order, its loaded speed, its empty speed — gives the landscape you described. Three properties make it useful: the attribution is **exact for the model**, it resolves **per solution** instead of averaging over a population, and it costs **one pass per schedule**. I can also check it: on any schedule that has been evaluated, recomputing the same split from the true durations agrees with what the surrogate gives. Pooled over sampled solutions the profile comes out assignment > sequence > loaded speed > empty speed, stable across sizes, with the AGV-side families carrying about three quarters of the mass, so these instances are transport-bound — a property the attribution reports directly and that I did not have to assume. One negative belongs with it: that pooled profile barely differs between Pareto-optimal and dominated solutions, so it characterises the instance and not why one solution beat another. That discrimination comes from the per-solution version and from the trade-off scores in point 4.

3. **Feedback algorithm.** The search is a surrogate-assisted NSGA-II. Each generation it over-produces offspring, ranks them with the surrogate, and sends only the best through to the exact evaluator, so the number of exact evaluations per generation is unchanged and every comparison I report is at a **matched exact-evaluation budget**. The attribution is then reused to steer the mutation: it says which task is currently binding, so that is where the operator is applied, and whether that task is bound by its transport or by its crane, which selects between reassigning or swapping vehicles and changing crane order. The same object that explains a schedule picks the next move. It outperforms my re-implementations of the metaheuristic baselines on all eleven instances in my test matrix, four of which are your Table 5 loading instances, and the advantage grows with instance size. Those re-implementations are mine rather than yours, so I am checking them against your published optima — Table 1 of the book chapter for the loading instances, and Table 2 of the FSMJ paper for the dual-cycling ones, where your mp-BRKGA results appear beside the MILP optima and I can compare my gap against yours on the same instances. I should add that every arm in my comparison is given the same generation count, well below the 300 generations you tuned mp-BRKGA to, so this is a comparison at equal budget and not against your published configuration.

4. **Pareto-front behaviour.** Doing the attribution at every point of the front, weighted by the local makespan–energy trade-off, ranks which tasks are the bottleneck at that point, and comparing the ends shows how the bottleneck moves. At the makespan end almost everything binding is AGV travel; at the energy end the vehicles are slowed, the cranes serialise behind them, and crane handlings become the binding activities. A small predictor given only an instance's fleet and crane structure then places a new instance on that axis without running the search — with one condition I should state plainly. On your published small set there is nothing to predict: the critical path is transport-bound almost everywhere (transport share 0.88 ± 0.04 between instances), so the predictor only ties a constant baseline there. I had to build a set spanning the fleet-to-crane ratio to test it at all, and on that set it recovers the transport share of unseen instances at r = 0.945, beating the constant baseline by a factor of 2.7. The saturation is itself worth knowing: for this layout, transport binding the critical path looks like a near-invariant property rather than something that varies by instance.

The physics is verified rather than assumed: Eqs (2)–(4) and (10)–(18) agree to zero discrepancy with an independent transcription, and on small instances with exhaustive enumeration of all speed assignments.

I would also like to request the data for the DL instances, which Section 5 of the FSMJ paper gives as downloadable from the FAST Manufacturing instance page. That page currently lists only the JSPT, FJSPT and JSPT+SR libraries, so I could not find the container terminal set there. Two parts of it would unblock me:

1. **The QC↔LU distance matrix for the DL layout.** Table 4 of the book chapter covers QC1–6 and LU1–6, and the DL instances have 8–16 cranes.
2. **The DL task lists**, once that geometry exists.

For the small instances I need nothing further, having reconstructed them from the book chapter: Table 5 gives the loading set directly, Section 5.1 the unloading set by reversing origins and destinations, and the combination column of Table 3 of the book chapter the twenty-six dual-cycling instances. The sizes that reconstruction produces agree with the Q-T column of Table 2 of the FSMJ paper on all twenty-six, so I believe it is faithful, but I would be glad to be corrected if any step is wrong. Above sixteen tasks I am still on instances I generate myself.

I would be grateful for your thoughts on the direction as a whole. If you would like the architecture changed, or any of the elements of the paper set up differently — the choice of surrogate, the way the comparisons are run, or what is being reported — please do tell me and I will adjust it.

One point I would particularly welcome your guidance on is the coupled regime with peak power constraints. I have taken the peak-power model from your ITOR paper and transferred it to the terminal: the fleet shares one instantaneous budget, travel legs draw power and crane handling draws none, and when the budget never binds the evaluator provably reduces to the uncoupled one. That regime is where the surrogate earns its place, the makespan there having no closed form, and it is also where the method wins by the clearest margin. Its one weakness is that the combination is not something you have published instances for, so those results stand on instances I generate. Since ITOR is set in job shop scheduling and neither of the terminal papers carries a power constraint, the extension is mine and not yours, and I would rather follow your judgement than my own on it: I am glad to keep the regime in the paper, or to set it aside and hold the work to the uncoupled problem on your published instances.

Any further direction on where you think the work should go next would be very welcome.

The codebase is accessible at this public repository https://github.com/aayushjha1729/e-hgatv2

Kind regards,
Aayush
