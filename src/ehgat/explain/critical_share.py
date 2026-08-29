"""Duration-weighted decomposition of the makespan over the critical path.

The makespan is a longest path under :math:`(\\max, +)`, so the durations of the activities its
subgradient selects sum to :math:`C_{\\max}` exactly -- the property asserted by
``tests/unit/test_tape.py::test_critical_path_durations_sum_to_makespan``. Apportioning that sum
between vehicle travel and crane handling therefore yields a share that is a genuine
decomposition of the objective rather than a tally of selected objects.

This matters because the two explanations being compared do not enumerate the same objects. The
model's subgradient marks *legs*, of which a task has two, while the exact bottleneck oracle of
:func:`ehgat.benchmark.faithfulness.critical_path_binding` partitions *tasks* by whichever
resource gated them; a task can also carry a critical handling while its vehicle chain binds,
because a loading move adds its handling after the maximum. Counting therefore produces two
quantities that are not comparable, and a discrepancy between them measures the definitions
rather than the model. Weighting by duration removes the ambiguity: each side apportions its own
makespan using its own durations and its own gradients, the two shares sum to one by
construction, and any residual difference is attributable to the model.

Bottleneck migration is expressed on the same footing, as the movement of that share between the
makespan-optimal and energy-optimal ends of a front, so it is likewise comparable across the
exact and learned explanations.
"""

from __future__ import annotations

from dataclasses import dataclass

from ehgat.environment.decoder import Schedule
from ehgat.environment.evaluator import evaluate
from ehgat.environment.instance import Instance
from ehgat.explain.tape_explainer import TapeExplanation, explain_schedule

__all__ = [
    "CriticalShares",
    "critical_path_shares",
    "exact_critical_shares",
    "migration",
]

_ON_PATH = 0.5  # a subgradient of a maximum is an indicator, so any interior cut separates it


@dataclass(frozen=True, slots=True)
class CriticalShares:
    """Apportionment of one schedule's makespan over its critical activities.

    ``transport`` and ``handling`` sum to one whenever the critical path carries any duration.
    ``total_duration`` is the summed duration of the selected activities and should agree with
    ``makespan`` to floating-point tolerance; a gap indicates the gradients and the durations were
    taken from different schedules.
    """

    transport: float
    handling: float
    total_duration: float
    makespan: float
    num_legs: int
    num_handlings: int

    @property
    def closes(self) -> bool:
        """Whether the selected durations reproduce the makespan."""
        return abs(self.total_duration - self.makespan) <= 1e-6 * max(1.0, abs(self.makespan))


def critical_path_shares(
    explanation: TapeExplanation,
    empty_time: tuple[float, ...],
    loaded_time: tuple[float, ...],
    handling_time: tuple[float, ...],
    *,
    threshold: float = _ON_PATH,
) -> CriticalShares:
    """Split ``explanation``'s critical path into travel and handling shares of the makespan.

    The three duration sequences must be the ones the explanation differentiated: the exact leg
    times for the oracle, and the model's predicted leg times for the fused explainer. Mixing
    them is what the ``closes`` check is for.
    """
    n = len(handling_time)
    if not (len(empty_time) == len(loaded_time) == n):
        raise ValueError(
            f"duration sequences disagree: empty={len(empty_time)}, "
            f"loaded={len(loaded_time)}, handling={n}"
        )

    travel = 0.0
    handling = 0.0
    n_legs = 0
    n_handlings = 0
    for j in range(n):
        if explanation.empty_time_grad[j] > threshold:
            travel += float(empty_time[j])
            n_legs += 1
        if explanation.loaded_time_grad[j] > threshold:
            travel += float(loaded_time[j])
            n_legs += 1
        if explanation.node_grad[j] > threshold:
            handling += float(handling_time[j])
            n_handlings += 1

    total = travel + handling
    return CriticalShares(
        transport=travel / total if total > 0.0 else float("nan"),
        handling=handling / total if total > 0.0 else float("nan"),
        total_duration=total,
        makespan=float(explanation.makespan),
        num_legs=n_legs,
        num_handlings=n_handlings,
    )


def exact_critical_shares(schedule: Schedule, instance: Instance) -> CriticalShares:
    """Shares taken from the exact tropical oracle, with no surrogate involved."""
    ev = evaluate(schedule, instance)
    ex = explain_schedule(schedule, instance)
    return critical_path_shares(
        ex,
        ev.empty_time,
        ev.loaded_time,
        tuple(task.handling_time for task in instance.tasks),
    )


def migration(makespan_end: CriticalShares, energy_end: CriticalShares) -> float:
    """Movement of the transport share between the two extremes of a front.

    Zero denotes a bottleneck whose composition is unchanged along the trade-off; one denotes a
    complete exchange between the two resources. Reported as a signed quantity would hide which
    end is transport-heavy, so the sign is kept: positive means the makespan-optimal end leans
    more on travel than the energy-optimal end does.
    """
    return float(makespan_end.transport - energy_end.transport)
