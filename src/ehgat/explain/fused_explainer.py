"""Pure-gradient extraction for the fused E-HGATv2 (the model-native TAPE).

Because :class:`~ehgat.explain.fused_ehgat.FusedEHGATv2` routes ``C_max`` through the exact
max-plus DP, ``dC_max/d(leg time)`` is a **binary critical-path indicator** with no
numerical smearing -- the network's own gradients *are* the explanation. This module:

- runs the fused model and extracts ``dC_max`` / ``dE`` w.r.t. the predicted local leg
  attributes, packaged as a :class:`~ehgat.explain.tape_explainer.TapeExplanation` (so the
  shared :func:`~ehgat.explain.pts_calculator.pareto_tension_scores` works unchanged), and
- validates **faithfulness** by comparing the fused model's critical path against the exact
  simulator-based TAPE oracle on the same schedule.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import torch

from ehgat.environment.decoder import Schedule
from ehgat.environment.instance import Instance
from ehgat.explain.fused_ehgat import FusedEHGATv2
from ehgat.explain.pts_calculator import ParetoPoint, pareto_tension_scores
from ehgat.explain.tape_explainer import (
    TapeExplanation,
    explain_schedule,
    explain_schedule_coupled,
)
from ehgat.surrogate.graph import AGV_EDGE, build_hetero_graph

__all__ = [
    "FaithfulnessReport",
    "explain_fused",
    "explain_fused_schedules",
    "faithfulness_report",
    "fused_pareto_tension_scores",
]


def _grad_tuple(t: torch.Tensor) -> tuple[float, ...]:
    if t.grad is None:
        return tuple(0.0 for _ in range(t.numel()))
    return tuple(float(v) for v in t.grad.detach())


def explain_fused(
    model: FusedEHGATv2, schedule: Schedule, instance: Instance
) -> TapeExplanation:
    """Extract the fused model's native tropical gradients as a :class:`TapeExplanation`.

    The returned ``empty_time_grad`` / ``loaded_time_grad`` / ``event_edge_grad`` are
    ``dC_max/d(predicted leg)`` -- exact binary critical-path indicators -- and the
    energy gradients are ``dE/d(predicted leg energy) = 1`` by additive construction.
    """
    model.eval()
    data = build_hetero_graph(schedule, instance)
    # Leg energies are read straight from the input arc features; make them differentiable
    # so dE/d(leg energy) propagates (it is exactly 1 by additive construction).
    data[AGV_EDGE].edge_attr.requires_grad_(True)
    out = model(data)

    for leaf in (out.empty_t, out.loaded_t, out.empty_e, out.loaded_e, out.node_delay):
        leaf.retain_grad()
    out.dag.edge_weights.retain_grad()

    out.makespan.backward(retain_graph=True)
    node_grad = _grad_tuple(out.node_delay)
    empty_time_grad = _grad_tuple(out.empty_t)
    loaded_time_grad = _grad_tuple(out.loaded_t)
    event_edge_grad = _grad_tuple(out.dag.edge_weights)

    # Leg energies feed both the makespan (via the leg-time prior) and the energy, so clear
    # their accumulated makespan grads before the energy pass to read a clean dE/d(leg)=1.
    for leaf in (out.empty_e, out.loaded_e):
        leaf.grad = None
    out.energy.backward()
    return TapeExplanation(
        makespan=float(out.makespan.detach()),
        energy=float(out.energy.detach()),
        node_grad=node_grad,
        empty_time_grad=empty_time_grad,
        loaded_time_grad=loaded_time_grad,
        empty_energy_grad=_grad_tuple(out.empty_e),
        loaded_energy_grad=_grad_tuple(out.loaded_e),
        event_edges=tuple(out.dag.meta),
        event_edge_grad=event_edge_grad,
        completion_nodes=tuple(int(v) for v in out.dag.completion_nodes.tolist()),
        surrogate_grad=None,
    )


def explain_fused_schedules(
    model: FusedEHGATv2, schedules: list[Schedule], instance: Instance
) -> list[TapeExplanation]:
    """Run the fused explainer over a Pareto set / final-generation schedule list."""
    return [explain_fused(model, s, instance) for s in schedules]


def fused_pareto_tension_scores(
    model: FusedEHGATv2, schedules: list[Schedule], instance: Instance
) -> list[dict[str, Any]]:
    """Compute Pareto Tension Scores from the fused model's native gradients."""
    points = [
        ParetoPoint(str(i), ex.makespan, ex.energy, ex)
        for i, ex in enumerate(explain_fused_schedules(model, schedules, instance))
    ]
    return pareto_tension_scores(points)


@dataclass(frozen=True, slots=True)
class FaithfulnessReport:
    """Agreement of the fused model's critical path with the exact TAPE oracle."""

    makespan_abs_error: float
    energy_abs_error: float
    leg_critical_jaccard: float
    arc_critical_jaccard: float

    def to_dict(self) -> dict[str, float]:
        return {
            "makespan_abs_error": self.makespan_abs_error,
            "energy_abs_error": self.energy_abs_error,
            "leg_critical_jaccard": self.leg_critical_jaccard,
            "arc_critical_jaccard": self.arc_critical_jaccard,
        }


def _critical_set(grads: tuple[float, ...], *, threshold: float = 0.5) -> set[int]:
    return {i for i, g in enumerate(grads) if g > threshold}


def _jaccard(a: set[int], b: set[int]) -> float:
    if not a and not b:
        return 1.0
    union = a | b
    return len(a & b) / len(union) if union else 1.0


def faithfulness_report(
    model: FusedEHGATv2, schedule: Schedule, instance: Instance
) -> FaithfulnessReport:
    """Compare the fused model's critical path to the exact simulator-based TAPE oracle.

    A ``leg_critical_jaccard`` near 1 means the fused (anchored) model recovers the *same*
    binding legs the exact max-plus oracle identifies -- i.e. faithful by construction once
    the local physical attributes are anchored.
    """
    fused = explain_fused(model, schedule, instance)
    # Under coupling the true critical path runs over the coupled activity DAG (leg+wait
    # effective weights); compare against the matching coupled oracle, not the uncoupled one.
    if instance.peak_power is not None:
        exact = explain_schedule_coupled(schedule, instance)
    else:
        exact = explain_schedule(schedule, instance)

    fused_legs = _critical_set(fused.empty_time_grad) | {
        i + len(fused.empty_time_grad) for i in _critical_set(fused.loaded_time_grad)
    }
    exact_legs = _critical_set(exact.empty_time_grad) | {
        i + len(exact.empty_time_grad) for i in _critical_set(exact.loaded_time_grad)
    }
    arc_fused = _critical_set(fused.event_edge_grad)
    arc_exact = _critical_set(exact.event_edge_grad)

    return FaithfulnessReport(
        makespan_abs_error=abs(fused.makespan - exact.makespan),
        energy_abs_error=abs(fused.energy - exact.energy),
        leg_critical_jaccard=_jaccard(fused_legs, exact_legs),
        arc_critical_jaccard=_jaccard(arc_fused, arc_exact),
    )
