# Reply to Prof. Homayouni — AI provenance and verification

> Working draft. Lives in the working repository only. It is not in the review tree the
> advisor reads, and must not be copied into it.
>
> Context: his reply of 11:24 asks which parts of the report and code were AI-generated
> and where I was in the loop. He has parked the substantive questions until this is
> answered, so this reply answers only that and closes by repeating the data request from
> the previous email.

---

Dear professor,

Thank you for the quick reply, and it is a fair question to ask first.

The implementation and the drafting of the report were both produced with AI assistance, and substantially so, and I used it as well to survey the deep learning literature for which families of surrogate suit a problem of this structure. What I did was direct it and verify it. The modelling was mine: I chose to follow the terminal model of your papers rather than the job-shop formulation, to keep the AGVs speed-adjustable, and to decide in each case what had to be tested and what would count as evidence. I also checked every claim in the report against the artifact it rests on before it was allowed to stand, and where I could not reproduce a number the claim came out.

The architecture I arrived at by ablation rather than by preference. The governing point is that the makespan here is a longest path through a disjunctive graph, and so a max-plus expression rather than an arbitrary function to be regressed. I built the XGBoost and TreeSHAP approach of your XAI and MOO plan first, on the same decision-variable encoding of sequencing and speed that you propose, and it is in the report as the comparison baseline; its limitation is that a fixed-width surrogate cannot be evaluated on an instance larger than the one it was fitted on, which is what closes off the size results. A homogeneous graph network lifts that restriction but is still wrong for this problem, since the physical quantities live on the arcs rather than the nodes. What remained was edge-conditioned attention over a heterogeneous graph with a differentiable max-plus head, so that the network learns only the physics of each leg while the head composes those legs into the makespan exactly, rather than the network having to learn the composition as well. Differentiating that head with respect to the legs the network itself predicted returns the critical path, and it is those attributions that guide the search, which keeps the method on the track you asked for while making the explanation exact rather than approximate. Each of your directives was then addressed against that design.

I can point you at the record rather than ask you to take my word for it. The repository has 126 commits over the last two months, of which 36 are corrections, retractions, or audits of my own earlier claims — among them one recording that a model I had built does not beat its constant baseline, and one retracting a negative result I had previously attributed to the guided method after finding it was the mp-BRKGA baseline spiking instead. There are 29 unit-test files covering the evaluator, the physics, the tropical gradient, and the mp-BRKGA implementation. `PAPER_FINDINGS.md` is a standing audit in which I hold each statement in the paper against the artifact behind it and record the gaps; `PROGRESS.md` records what has not been run.

A few specific things I checked by hand against your papers: that the three speed levels carry your values exactly; that the energy objective covers AGV travel only and not crane handling, as you state it; and that our mp-BRKGA follows your published operators and population structure, though I run it at a smaller budget than yours.

I should also say plainly that some of the report is not yet settled, and I have marked those places rather than smoothed them over. The peak-power extension is mine and not taken from your terminal papers, so it runs on instances I generate. One structural measure in the front section needs its definition reconciled before I would quote the number. And above sixteen tasks I am still on instances of my own.

That last point is why I would be grateful for the DL instance data I asked about in my previous email. Two parts of it would unblock me: the QC-to-LU distance matrix for the DL layout, since Table 4 of the book chapter covers only QC1–6 and LU1–6 while the DL instances have 8 to 16 cranes, and then the DL task lists.

I would be glad to walk you through any part of it in person and to show the derivation or the run behind any number you want to test.

Kind regards,
Aayush
