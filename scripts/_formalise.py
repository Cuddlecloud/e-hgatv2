"""Raise the register of the thesis to a consistently formal academic voice.

Removes interrogative headings and captions, editorial asides, and the negative construction
stating what the formulation does not contain. Declarative statements replace rhetorical framing.
"""

from pathlib import Path

P = Path("thesis/main.tex")
s = P.read_text()

subs: list[tuple[str, str]] = [
    (
        r"\subsection{Why a surrogate, and why this class of surrogate}",
        r"\subsection{Selection of the surrogate model class}",
    ),
    (
        "\\caption{Why the head, and not the encoder, determines faithfulness. (a) A pooled regression head\n"
        "mixes every node embedding into the output, so the Jacobian is dense and credit is assigned to\n"
        "activities that provably cannot affect $\\Cmax$. (b) The max-plus layer records the maximising\n"
        "predecessor of each node in the forward pass and routes the subgradient exclusively through it, so\n"
        "the attribution is the critical path itself.}",
        "\\caption{The output head, rather than the encoder, determines the faithfulness of the\n"
        "attribution. (a) A pooled regression head mixes every node embedding into the output, producing a\n"
        "dense Jacobian that assigns credit to activities which provably cannot affect $\\Cmax$. (b) The\n"
        "max-plus layer records the maximising predecessor of each node during the forward pass and routes\n"
        "the subgradient exclusively through it, so that the attribution coincides with the critical\n"
        "path.}",
    ),
    (
        "Resource bindings are therefore functions of the task, not assignment variables, and sequencing is\n"
        "represented by the order of tasks within a resource's chain. No binary decision variables or\n"
        "big-$M$ constraints appear anywhere in this thesis: the formulation below is stated directly as\n"
        "the timing recurrences that a resolved schedule satisfies, which is both what the implementation\n"
        "computes and what makes the max-plus structure of Section~\\ref{sec:maxplus} visible. A\n"
        "mixed-integer programme for the same problem exists \\citep{fontes2023} and is what supplies the\n"
        "published optima used for verification in Section~\\ref{sec:evaluation}, but it plays no part in\n"
        "the method.",
        "Resource bindings are functions of the task, and sequencing is represented by the order of tasks\n"
        "within a resource's chain. The formulation adopted below states the problem as the timing\n"
        "recurrences that a resolved schedule satisfies. This is the form the implementation computes and\n"
        "the form in which the max-plus structure of Section~\\ref{sec:maxplus} is manifest. The\n"
        "mixed-integer programme of \\citet{fontes2023} formulates the same problem and supplies the\n"
        "published optima used for verification in Section~\\ref{sec:evaluation}; the method developed here\n"
        "operates on the recurrences directly.",
    ),
    (
        "The subsequent question is less well studied. An operator receives a front and must select from\nit.",
        "The subsequent question has received less attention. An operator receives a front and must\nselect from it.",
    ),
    (
        "The makespan is less direct. Fixing the assignment and the sequencing turns the schedule into a\n"
        "precedence graph:",
        "The makespan requires the precedence structure. Fixing the assignment and the sequencing turns\n"
        "the schedule into a precedence graph:",
    ),
    (
        "This asymmetry is worth stating plainly because it inverts the usual reading of an attentional\n"
        "graph network, in which the within-neighbourhood attention is the object of interest. Here that\n"
        "component is structurally vacuous and the cross-type component carries the resource-contention\n"
        "signal.",
        "This asymmetry inverts the conventional reading of an attentional graph network, in which the\n"
        "within-neighbourhood attention constitutes the object of interest. In the present setting that\n"
        "component is structurally vacuous, and the cross-relation component carries the\n"
        "resource-contention signal.",
    ),
    (
        "\\paragraph{An honest reading of the energy result.} The pooled arc features that the encoder\n"
        "aggregates include the per-leg energies themselves.",
        "\\paragraph{Interpretation of the energy prediction.} The pooled arc features that the encoder\n"
        "aggregates include the per-leg energies themselves.",
    ),
    (
        "Counting on-path activities of each kind is inadequate, and the reason is instructive. Legs and\n"
        "handlings are not commensurable:",
        "Counting on-path activities of each kind is inadequate. Legs and handlings are not\ncommensurable:",
    ),
    (
        "Two features merit comment. Every on-path activity belongs to the same vehicle, indicating that\n"
        "this schedule is vehicle-limited and that the pertinent intervention is fleet capacity rather than\n"
        "crane rebalancing. And the division between travel and handling is quantified rather than\n"
        "asserted: $\\rho = 0.714$ indicates that slightly over seventy per cent of the makespan consists\n"
        "of vehicle movement and the remainder of crane handling. This is the form of statement the thesis\n"
        "set out to produce.",
        "Two properties of this traversal are of note. Every on-path activity belongs to the same vehicle,\n"
        "which establishes that the schedule is vehicle-limited and that the pertinent intervention is\n"
        "fleet capacity rather than crane rebalancing. The division between travel and handling is\n"
        "quantified rather than asserted: $\\rho = 0.714$ indicates that slightly over seventy per cent of\n"
        "the makespan consists of vehicle movement and the remainder of crane handling. This constitutes\n"
        "the form of statement the thesis set out to produce.",
    ),
    (
        "The salient observation is the near-absence of migration: mean absolute migration is $0.047$, and\n"
        "the transport share lies between $0.91$ and $1.00$ at \\emph{both} ends of every front. Taken\n"
        "alone this is a negative result for the hypothesis that the bottleneck migrates.",
        "Migration is near-absent throughout: mean absolute migration is $0.047$, and the transport share\n"
        "lies between $0.91$ and $1.00$ at \\emph{both} ends of every front. Considered in isolation this\n"
        "constitutes a negative result for the hypothesis that the bottleneck migrates.",
    ),
    (
        "The sign is informative and identifies the direction of the transfer.",
        "The sign identifies the direction of the transfer.",
    ),
    (
        "The mechanism is direct. Minimising the makespan drives every leg to the fastest available speed,",
        "The mechanism follows from the speed selection. Minimising the makespan drives every leg to the\n"
        "fastest available speed,",
    ),
]

for i, (old, new) in enumerate(subs, 1):
    if old not in s:
        raise SystemExit(f"substitution {i} did not match; aborting with no changes written")
    s = s.replace(old, new, 1)

P.write_text(s)
print(f"applied {len(subs)} register corrections")
