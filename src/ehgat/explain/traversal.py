"""Exact critical-path traversal and its additive makespan decomposition.

This is the **required** explanation tier: it answers "why is this solution Pareto-optimal?"
using the exact max-plus oracle in :mod:`ehgat.explain.tape_explainer` and **no network at
all**. The surrogate's post-hoc reproduction of the same traversal is a separate and strictly
weaker claim and lives in :mod:`ehgat.explain.fused_explainer`; the two are reported separately,
so that the accuracy of the surrogate does not qualify a result that is independent of it.

The decomposition is exact by construction rather than by fit. Because the makespan is a
max-plus longest path, every on-path activity carries a binary subgradient
``dC_max/d(duration) = 1``, so the on-path durations sum to ``C_max`` identically::

    C_max = sum of on-path leg durations + sum of on-path QC handlings

:func:`exact_traversal` asserts that identity rather than assuming it, so a silent change in the
evaluator or the oracle surfaces here as ``closes=False`` instead of propagating into a table.
"""

from __future__ import annotations

from dataclasses import dataclass

from ehgat.environment.decoder import Schedule
from ehgat.environment.evaluator import evaluate
from ehgat.environment.instance import Instance
from ehgat.explain.tape_explainer import explain_schedule

__all__ = ["ExactTraversal", "OnPathActivity", "exact_traversal", "on_path"]

# An activity is on the critical path iff its subgradient exceeds this. The subgradient of a
# max is an indicator, so the true values are 0 or 1 and the threshold is only guarding against
# floating-point dust; it is deliberately the same 0.5 the fused explainer uses, so the two
# tiers are compared on an identical definition of "on-path".
_ON_PATH = 0.5

# Relative tolerance for the decomposition identity. The sum is over on-path durations read from
# the same evaluation that produced the makespan, so anything above rounding noise is a defect.
_TOL = 1e-6


def on_path(grads: tuple[float, ...], threshold: float = _ON_PATH) -> set[int]:
    """Indices whose subgradient marks them as critical-path members."""
    return {j for j, g in enumerate(grads) if g > threshold}


@dataclass(frozen=True, slots=True)
class OnPathActivity:
    """One binding activity, ordered as the schedule executes it."""

    task: int
    activity: str  # "empty_leg" | "loaded_leg" | "qc_handling"
    duration: float
    dcmax: float  # the subgradient; 1.0 for an on-path activity
    completion: float  # the task's completion time, used only to order the traversal
    agv: int
    qc: str


@dataclass(frozen=True, slots=True)
class ExactTraversal:
    """The exact critical path of one schedule, with its additive decomposition."""

    label: str
    makespan: float
    energy: float
    activities: tuple[OnPathActivity, ...]
    decomposition_total: float

    @property
    def path_len(self) -> int:
        return len(self.activities)

    @property
    def closes(self) -> bool:
        """Whether the on-path durations reproduce the makespan, as they must."""
        return abs(self.decomposition_total - self.makespan) <= _TOL * max(1.0, abs(self.makespan))

    @property
    def travel_total(self) -> float:
        return sum(a.duration for a in self.activities if a.activity != "qc_handling")

    @property
    def handling_total(self) -> float:
        return sum(a.duration for a in self.activities if a.activity == "qc_handling")


def exact_traversal(label: str, schedule: Schedule, instance: Instance) -> ExactTraversal:
    """Traverse the exact makespan critical path of ``schedule``.

    Uses only the exact oracle -- no surrogate is constructed, loaded or consulted. Activities
    are ordered by the completion time of the task that owns them, so the result reads forwards
    from the start of the schedule to the task that defines the makespan.
    """
    ev = evaluate(schedule, instance)
    oracle = explain_schedule(schedule, instance)

    # AGV assignment per task, for attributing each binding activity to a vehicle.
    activities: list[OnPathActivity] = []
    total = 0.0
    for j in range(instance.num_tasks):
        completion = float(ev.completion[j])
        agv = int(schedule.assignment[j])
        qc = instance.tasks[j].qc
        for grad, name, duration in (
            (oracle.empty_time_grad[j], "empty_leg", float(ev.empty_time[j])),
            (oracle.loaded_time_grad[j], "loaded_leg", float(ev.loaded_time[j])),
            (oracle.node_grad[j], "qc_handling", float(instance.tasks[j].handling_time)),
        ):
            if grad <= _ON_PATH:
                continue
            activities.append(
                OnPathActivity(
                    task=j,
                    activity=name,
                    duration=duration,
                    dcmax=float(grad),
                    completion=completion,
                    agv=agv,
                    qc=qc,
                )
            )
            total += duration

    activities.sort(key=lambda a: (a.completion, a.task, a.activity))
    return ExactTraversal(
        label=label,
        makespan=float(oracle.makespan),
        energy=float(oracle.energy),
        activities=tuple(activities),
        decomposition_total=total,
    )
