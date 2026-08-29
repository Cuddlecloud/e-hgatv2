# Advisor Brief — Prof. Mahdi Homayouni (verbatim requirements)

> **READ EMAIL 3 FIRST. It supersedes everything below it.** The summary and Emails 1–2
> are kept as history, not as instructions. Measuring the thesis against them produces
> false gaps: they call for R3 scalability, amortization and the peak-power–coupled
> regime, and Email 3 retires all three explicitly.

---

## Email 3 — 20 August 2026, "Re: Summer thesis supervision request" (CURRENT DIRECTION)

Transcribed from the message; the visible text ends mid-sentence in the final paragraph.

> I really appreciate your efforts during the design and experiment process. My main concern
> is not whether the work contains useful results, but that the current draft combines **too
> many** different ideas and becomes unnecessarily hard to follow for a bachelor thesis. One
> thing came to my mind immediately was that you imported all the papers I sent you and the
> ideas and tried to mix them all together. This is not bad, but it became "over-engineered"
> and thus hard to be understood.
>
> Particularly, you were not supposed to mix "the QC + SA-AGV bi-objective scheduling problem"
> with "power-constrained scheduling idea from manufacturing" just to complicate the problem
> (I'll explain this to you when we meet in-person).
>
> I highly advise that you narrow down the thesis on one clear core idea. You don't need to
> redo anything, but you need to revise the text. Based on the current draft and the results,
> the strongest and most understandable focus would be:
>   1. solve the original scheduling problem (without power constraints),
>   2. use the surrogate as a supporting tool,
>   3. and explain why selected solutions are Pareto-optimal.
>
> Feedback loop into the algorithm is a great idea and I definitely invite you to work on it.
> But, we must do it in steps. Therefore, the surrogate model will have a secondary role as a
> post-hoc explanation tool for finalized solutions, or as a way to compare how explanations
> change during the search. The second idea may need new experiments, and thus, I would ask
> you do it if time allows. The post-hoc explanation is already over the requirements of this
> thesis.
>
> And finally, I expect you to be able to explain and understand every single detail and step
> in the whole methodology. So, keep it simple but scientific.
>
> I already added a few comments to your PDF. Remember that AI usually write it bad and you
> must direct it to write correctly. For example, the introduction must explain why this
> specific problem (e.g., explaining the Pareto-optimal solutions) is significant to be
> studied, and how novel it is. Also, what is the main contribution of the thesis. And, for a
> bachelor thesis, it must not be too complicated that is not understandable easily.

### What Email 3 requires, and where the thesis answers it

| requirement | where |
|---|---|
| 1. the original scheduling problem, **no power constraints** | throughout; the coupled regime is excluded and named as future work in Ch. 5 |
| 2. surrogate as a **supporting tool** | §4.7 calibration and faithfulness; the exact oracle is the yardstick |
| 3. **explain why solutions are Pareto-optimal** | §4.2 worked example, §4.3–§4.5 the migration result |
| surrogate role (a): post-hoc explanation of finalised solutions | §4.7 — he calls this "already over the requirements" |
| surrogate role (b): how explanations change during the search | §4.6 — the "if time allows" item, done |
| significance / novelty / contribution, separately, in the introduction | §1.1, §1.2, §1.3 |
| "keep it simple but scientific"; explainable in every detail | one core idea stated in §1.3; everything else subordinated to it |

### What Email 3 retires

Do not reintroduce these, and do not score the thesis against them:

- **Peak-power–coupled regime.** Named as the specific thing that should not have been mixed in.
  Note that the `SD-N` instance series in `paper/main.tex` is entangled with it
  (`toy10_pp30` → `"SD-10-C"` in `scripts/emit_r3_numbers.py`), so material from that paper's
  §5.5 cannot be ported into the thesis without dragging the coupled strand back in.
- **R3 scalability against stalling non-GNN baselines**, and **R4 amortization.** Superseded by
  "use the surrogate as a supporting tool" in a "secondary role".
- **The feedback loop / attribution-guided search.** Explicitly deferred by him: "we must do it
  in steps."

### Standing cautions from Email 3

- `SD-N` names are synthetic toys, not published instances (`toy10` → `"SD-10"`). Worked examples
  in the thesis must use the published sets.
- "AI usually write it bad and you must direct it to write correctly" — he is reading for
  over-complication and for text that asserts more than the evidence supports.

---

## HISTORY BELOW — superseded by Email 3

> Superseded framing, kept for the record: the results were once expected to show
> scalability and amortization benefits for R3 where standard non-GNN methods (random
> NSGA-II, mp-BRKGA) stall, the same in the peak-power–coupled regime, and R1 satisfied
> by natively encoding the problem features. The interpretability / attention-faithfulness
> / Viterbi track is a separate later fork (TMLR/ICLR), not this paper.

## What the OR paper must demonstrate (owner's summary of the brief)
1. **R3 scalability** — guided optimization retains its advantage as N grows, where
   standard non-GNN methods (random NSGA-II, mp-BRKGA) stall.
2. **Amortization benefits** — the surrogate learns Pareto-front behaviour and reuses
   knowledge gathered during search (search → knowledge loop).
3. **Peak-power–coupled regime** — the same scalability and amortization advantages hold
   under the coupled power constraint, not only in the uncoupled setting.
4. **R1** — natively encoding the problem features (physics-fused heterogeneous encoding).

## Email 1 — three research directions
Dear Aayush,

I am attaching three of my recent works to this email. The 2023'... and 2022'... works
help you understand the problem. The "Homayouni_XAI+MOO" work is a primary plan for
research I designed to specifically work on multi-objective optimization (MOO).

You can design your thesis in three directions, as we discussed before:

- An algorithm for **Feature Engineering** for this specific problem. I believe it will be
  based on post-hoc analysis for a set of given problem instances. Then, we evaluate this
  algorithm for a larger set of problem instances. Here you can propose to use XAI (any
  method) or causal-ML, or any other cause-analysis method.
- A **feature importance analysis** for the small-sized problems based on post-hoc
  analysis. This would result in a kind of landscape analysis. I mean we want to design an
  algorithm that helps us to understand the relationship between the input variables (in
  our problem, for example, the order of tasks for each AGV, the travelling speed of AGV,
  the workload of cranes, etc.) and the objective function values. This would help us to
  explain why specific solutions are identified as Pareto (near-)Optimal.
- This would be the ultimate goal of the "Homayouni_XAI+MOO" work. To design a **feedback
  algorithm** for the optimization algorithm which helps it to search in a specific
  neighbourhood, or select a specific heuristic mechanism, or ...

Also, one of my ex-students has designed a **discrete-event simulation model** for a
container terminal. This would also be helpful in points 1 and 2 above. But needs more
thinking to include it in the research design.

See you,

## Email 2 — methodology latitude
Hi,

Take your time to read the papers and understand the problem.

For the methodology, you are free to design your own. I just would like to keep it in the
same track (**guiding the optimization algorithm**) using knowledge / explanation /
pattern gathered during the search.

One other aspect of this method is to extract this knowledge in a way the **surrogate model
learns the Pareto Front behaviour**.

Best,
Mahdi

## How our work maps to the brief
- **Direction 3 (feedback algorithm)** is the primary track: TAPE / attention guidance
  steers NSGA-II toward productive neighbourhoods (R3).
- **"Surrogate learns the Pareto-front behaviour"** is R4 amortization (front-composition
  recovery, between-instance corr 0.945 on the composition-diverse set).
- **Direction 2 (feature-importance / landscape)** is R1/R2: native feature encoding +
  critical-path attribution relating input variables (AGV order/speed, crane workload) to
  objectives.
- The discrete-event simulation model is a possible future validation asset (not yet
  integrated).
