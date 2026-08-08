# Advisor Brief — Prof. Mahdi Homayouni (verbatim requirements)

> Authoritative record of the advisor's stated direction for this thesis. This is an
> **OR paper first**: the results must be demonstrably valuable to an OR advisor —
> scalability and amortization benefits for R3 where standard non-GNN methods (random
> NSGA-II, mp-BRKGA) stall, the same in the peak-power–coupled regime, and R1 satisfied
> by natively encoding the problem features. The interpretability / attention-faithfulness
> / Viterbi track is a **separate later fork** (TMLR/ICLR), not this paper.

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
