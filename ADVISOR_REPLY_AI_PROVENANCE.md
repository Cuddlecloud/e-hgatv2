# Reply to Prof. Homayouni — AI provenance and verification

> Working draft. Lives in the working repository only. It is not in the review tree the
> advisor reads, and must not be copied into it.
>
> Context: his reply of 11:24 asks which parts of the report and code were AI-generated and
> where he was in the loop. He has parked the substantive questions until this is answered,
> so this reply answers only that and closes by repeating the data request.
>
> Verified figures: 126 commits, 36 of them corrections/retractions/audits (not 40).
> Venues: GAT is ICLR 2018, GATv2 ICLR 2022, HAN WWW 2019, Mensch and Blondel ICML 2018.

---

Dear professor,

I used AI to survey the deep learning literature and determine which families of surrogate
suit a problem of this structure — the graph attention line (ICLR 2018 and its 2022
revision), heterogeneous graph attention (WWW 2019), and the differentiable dynamic
programming work (ICML 2018). The core architectural and modelling choices were mine, and I
arrived at them through several ablation studies that I directed throughout. I chose to
follow the container terminal model of your papers rather than the job shop formulation,
kept the AGVs speed-adjustable, and decided in each case what had to be tested and what
would count as evidence before any claim was allowed into the report.

Across effectively the whole codebase — the evaluator, the E-HGATv2 surrogate, the tropical
attribution layer, the NSGA-II and mp-BRKGA implementations, and the benchmark harnesses and
unit tests — I used AI to generate and refactor code and to automate the manual scripting,
refactoring by hand where that was necessary. I also used it to run those harnesses, the
ablation studies and the validation runs on the VM, and to draft and format the report. What
remains mine is the methodology, the design of the ablations, and the interpretation and
synthesis of the results.

I checked the contents rather than accepting them. The working repository holds 126 commits
over the last two months, 36 of which are corrections, retractions, or audits of my own
earlier claims — including one recording that a model I had built does not beat its constant
baseline, and one retracting a negative result I had attributed to the guided method after
finding it was the mp-BRKGA baseline spiking instead.

I would be glad to explain the project in person at a time of your convenience.

I would also be grateful if you could kindly provide the DL instance data I asked about in
my previous email. Two parts of it would unblock me: the QC-to-LU distance matrix for the DL
layout, since Table 4 of the book chapter covers only QC1–6 and LU1–6 while the DL instances
have 8 to 16 cranes, and then the DL task lists.

Kind regards,
Aayush Jha
