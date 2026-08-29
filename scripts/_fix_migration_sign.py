"""One-off: correct the migration sign convention and its interpretation in the thesis.

The implementation defines migration as ``makespan_end.transport - energy_end.transport``
(``ehgat.explain.critical_share.migration``), but the thesis originally documented the opposite
and drew the opposite conclusion about which resource binds at which end. The data are
unambiguous: at L21, A/Q = 1.67, rho_mk = 0.230 and rho_en = 0.899, so the makespan-optimal end is
handling-bound and the energy-optimal end is travel-bound.
"""

from pathlib import Path

P = Path("thesis/main.tex")
s = P.read_text()
subs: list[tuple[str, str]] = []

subs.append((
    r"""The quantity of interest is the shift in $\rho_{\text{transport}}$ between the two ends of the
front,
\begin{equation}
\text{migration} = \rho_{\text{transport}}(\text{energy-optimal})
                 - \rho_{\text{transport}}(\text{makespan-optimal}).
\label{eq:migration}
\end{equation}
A negative value indicates that as energy is prioritised the bottleneck moves from vehicle travel
towards crane handling; a positive value indicates the converse; a value near zero indicates that
the nature of the bottleneck is invariant along the front even though the objective values are
not.""",
    r"""The quantity of interest is the shift in $\rho_{\text{transport}}$ between the two ends of the
front,
\begin{equation}
\text{migration} = \rho_{\text{transport}}(\text{makespan-optimal})
                 - \rho_{\text{transport}}(\text{energy-optimal}).
\label{eq:migration}
\end{equation}
The sign is retained rather than taken in absolute value, because it identifies \emph{which} end is
travel-heavy. A negative value indicates that the energy-optimal end leans more on travel than the
makespan-optimal end does, so that prioritising energy moves the bottleneck \emph{towards} vehicle
travel; a positive value indicates the converse; and a value near zero indicates that the character
of the bottleneck is invariant along the front even though the objective values are not."""))

subs.append((
    r"""The sign is informative. Where migration is substantial it is negative, indicating that the
bottleneck moves \emph{towards crane handling} as energy is prioritised. This is the predicted
mechanism: slowing the vehicles lengthens the travel legs, but the crane chains, whose handling
times are fixed and independent of vehicle speed, eventually dominate the residual. The single
instance exhibiting the opposite sign, L01 at $A/Q = 1.00$ with $+0.108$, is the four-task
instance, whose 35-point front offers too few structurally distinct schedules for the asymptotic
argument to apply.""",
    r"""The sign is informative, identifying the direction of the transfer. Where migration is
substantial it is negative, so by Eq.~\eqref{eq:migration} the energy-optimal end is the
travel-heavy one and the bottleneck moves \emph{towards vehicle travel} as energy is prioritised.
Figure~\ref{fig:front} makes this concrete: at the makespan-optimal end of L21 at $A/Q = 1.67$ the
critical path is only $23.0$ per cent travel and therefore predominantly crane handling, whereas at
the energy-optimal end it is $89.9$ per cent travel.

The mechanism is direct. Minimising the makespan drives every leg to the fastest available speed,
compressing travel until the crane chains --- whose handling times are fixed and independent of
vehicle speed --- become binding. Minimising energy does the reverse, selecting slow speeds that
lengthen every leg until travel dominates the path again. The cranes therefore bind at the fast end
and the vehicles at the slow end, which is why the transfer requires enough vehicles for the cranes
to be competitive at all, and why it vanishes below $A/Q \approx 1$.

The single instance whose sign is inverted relative to its neighbours, L01 at $A/Q = 1.00$, is the
four-task instance, whose 35-point front offers too few structurally distinct schedules for the
argument to apply."""))

subs.append((
    r"""instance--fleet cells under a Holm-corrected Wilcoxon signed-rank test, attaining $-0.662$ at
$A/Q = 1.67$, and vanishing below $A/Q \approx 1$ where both ends of the front are
transport-bound.""",
    r"""instance--fleet cells under a Holm-corrected Wilcoxon signed-rank test, attaining a magnitude
of $0.662$ at $A/Q = 1.67$, and vanishing below $A/Q \approx 1$ where both ends of the front are
transport-bound. Where the transfer occurs, the cranes bind at the makespan-optimal end and the
vehicles at the energy-optimal end."""))

subs.append((
    r"""significantly non-zero in 43 of 54 instance--fleet cells and attains $-0.662$; below
$A/Q \approx 1$ it vanishes, both front extremes being transport-bound.""",
    r"""significantly non-zero in 43 of 54 instance--fleet cells and attains a magnitude of $0.662$;
below $A/Q \approx 1$ it vanishes, both front extremes being transport-bound. Where it occurs, the
cranes bind at the makespan-optimal end and the vehicles at the energy-optimal end."""))

subs.append((
    r"""The empirical finding is that the explanation is not static along the front. Where vehicles are
sufficiently plentiful, trading time for energy transfers the binding constraint from vehicles to
cranes by an amount reaching two-thirds of the critical path.""",
    r"""The empirical finding is that the explanation is not static along the front. Where vehicles are
sufficiently plentiful, trading time for energy transfers the binding constraint from the cranes to
the vehicles by an amount reaching two-thirds of the critical path."""))

subs.append((
    r"""share of each. At the makespan-optimal end the critical path is almost entirely crane handling
($\rho_{\text{transport}} = 0.336$); at the energy-optimal end it is almost entirely vehicle
travel. The share, not the objective value, is what the explanation reports.}""",
    r"""share of each. At the makespan-optimal end the critical path is predominantly crane handling
($\rho_{\text{transport}} = 0.230$); at the energy-optimal end it is predominantly vehicle travel
($\rho_{\text{transport}} = 0.899$). The share, not the objective value, is what the explanation
reports.}"""))

for i, (old, new) in enumerate(subs, 1):
    if old not in s:
        raise SystemExit(f"substitution {i} did not match; aborting with no changes written")
    s = s.replace(old, new, 1)

P.write_text(s)
print(f"applied {len(subs)} substitutions to {P}")
