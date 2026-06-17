"""TAPE extraction engine: exact tropical gradients for resolved schedules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import torch
from torch import Tensor, nn

from ehgat.environment.decoder import Schedule
from ehgat.environment.evaluator import build_precedence
from ehgat.environment.instance import Instance, TaskKind
from ehgat.environment.physics import leg_energy, travel_time
from ehgat.explain.tropical_dp import tropical_longest_path
from ehgat.surrogate.graph import AGV_EDGE, NODE_TYPE, QC_EDGE, build_hetero_graph

__all__ = ["TapeExplanation", "explain_schedule", "explain_schedules", "surrogate_feature_gradients"]


@dataclass(frozen=True, slots=True)
class TapeExplanation:
    """Gradients of exact tropical makespan and additive energy for one schedule."""

    makespan: float
    energy: float
    node_grad: tuple[float, ...]
    empty_time_grad: tuple[float, ...]
    loaded_time_grad: tuple[float, ...]
    empty_energy_grad: tuple[float, ...]
    loaded_energy_grad: tuple[float, ...]
    event_edges: tuple[dict[str, Any], ...]
    event_edge_grad: tuple[float, ...]
    completion_nodes: tuple[int, ...]
    surrogate_grad: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "objectives": {"makespan": self.makespan, "energy": self.energy},
            "tropical": {
                "node_grad": list(self.node_grad),
                "empty_time_grad": list(self.empty_time_grad),
                "loaded_time_grad": list(self.loaded_time_grad),
                "event_edge_grad": list(self.event_edge_grad),
                "event_edges": list(self.event_edges),
                "completion_nodes": list(self.completion_nodes),
            },
            "energy": {
                "empty_energy_grad": list(self.empty_energy_grad),
                "loaded_energy_grad": list(self.loaded_energy_grad),
            },
            "surrogate_grad": self.surrogate_grad,
        }


def _leg_tensors(schedule: Schedule, instance: Instance, *, dtype: torch.dtype) -> tuple[Tensor, ...]:
    empty_t, loaded_t, empty_e, loaded_e = [], [], [], []
    agv_prev, _qc_prev, _ = build_precedence(schedule.agv_sequences, schedule.qc_sequences, instance.num_tasks)
    for j, task in enumerate(instance.tasks):
        origin = instance.agv_start if agv_prev[j] < 0 else instance.tasks[agv_prev[j]].dropoff
        empty_d = instance.distance.distance(origin, task.pickup)
        loaded_d = instance.loaded_distance(task)
        empty_t.append(travel_time(empty_d, schedule.empty_speed[j], loaded=False))
        loaded_t.append(travel_time(loaded_d, schedule.loaded_speed[j], loaded=True))
        empty_e.append(leg_energy(empty_d, schedule.empty_speed[j], loaded=False))
        loaded_e.append(leg_energy(loaded_d, schedule.loaded_speed[j], loaded=True))
    leaves = [torch.tensor(v, dtype=dtype, requires_grad=True) for v in (empty_t, loaded_t, empty_e, loaded_e)]
    return tuple(leaves)  # type: ignore[return-value]


def _event_dag(
    schedule: Schedule, instance: Instance, empty_t: Tensor, loaded_t: Tensor, *, dtype: torch.dtype
) -> tuple[Tensor, Tensor, Tensor, list[dict[str, Any]], Tensor]:
    """Expanded exact DAG: source plus per-task max, QC-finish and AGV-free events."""
    n = instance.num_tasks
    agv_prev, qc_prev, _ = build_precedence(schedule.agv_sequences, schedule.qc_sequences, n)
    source = 0

    def m(j: int) -> int: return 1 + 3 * j
    def q(j: int) -> int: return 1 + 3 * j + 1
    def a(j: int) -> int: return 1 + 3 * j + 2
    def prev_a(j: int) -> int: return source if agv_prev[j] < 0 else a(agv_prev[j])
    def prev_q(j: int) -> int: return source if qc_prev[j] < 0 else q(qc_prev[j])

    edge_src: list[int] = []
    edge_dst: list[int] = []
    weights: list[Tensor] = []
    meta: list[dict[str, Any]] = []
    completion_nodes: list[int] = []
    node_weights = torch.zeros(1 + 3 * n, dtype=dtype)
    for j, task in enumerate(instance.tasks):
        node_weights[q(j)] = task.handling_time
        if task.kind is TaskKind.LOAD:
            agv_arrival = empty_t[j] + loaded_t[j]
            completion_nodes.append(q(j))
            arcs = [
                (prev_a(j), m(j), agv_arrival, "agv_to_gate"),
                (prev_q(j), m(j), empty_t.new_zeros(()), "qc_to_gate"),
                (m(j), q(j), empty_t.new_zeros(()), "handling"),
                (prev_a(j), a(j), agv_arrival, "agv_free_load"),
            ]
        else:
            completion_nodes.append(a(j))
            arcs = [
                (prev_a(j), m(j), empty_t[j], "agv_to_gate"),
                (prev_q(j), m(j), empty_t.new_zeros(()), "qc_to_gate"),
                (m(j), q(j), empty_t.new_zeros(()), "handling"),
                (q(j), a(j), loaded_t[j], "agv_free_unload"),
            ]
        for u, v, w, kind in arcs:
            edge_src.append(u); edge_dst.append(v); weights.append(w)
            meta.append({"src": u, "dst": v, "task": j, "kind": kind})
    edge_index = torch.tensor([edge_src, edge_dst], dtype=torch.long)
    edge_weights = torch.stack(weights)
    return node_weights.requires_grad_(True), edge_index, edge_weights, meta, torch.tensor(completion_nodes)


def explain_schedule(
    schedule: Schedule, instance: Instance, model: nn.Module | None = None, *, dtype: torch.dtype = torch.float64
) -> TapeExplanation:
    """Extract exact TAPE gradients; optionally attach frozen-surrogate feature gradients."""
    empty_t, loaded_t, empty_e, loaded_e = _leg_tensors(schedule, instance, dtype=dtype)
    node_w, edge_index, edge_w, meta, completion_nodes = _event_dag(
        schedule, instance, empty_t, loaded_t, dtype=dtype
    )
    x = tropical_longest_path(node_w, edge_index, edge_w)
    makespan = x[completion_nodes].max()
    energy = (empty_e + loaded_e).sum()

    makespan.backward(retain_graph=True)
    node_grad = tuple(float(v) for v in node_w.grad.detach())
    edge_grad = tuple(float(v) for v in edge_w.grad.detach())
    empty_time_grad = tuple(float(v) for v in empty_t.grad.detach())
    loaded_time_grad = tuple(float(v) for v in loaded_t.grad.detach())

    energy.backward()
    return TapeExplanation(
        makespan=float(makespan.detach()),
        energy=float(energy.detach()),
        node_grad=node_grad,
        empty_time_grad=empty_time_grad,
        loaded_time_grad=loaded_time_grad,
        empty_energy_grad=tuple(float(v) for v in empty_e.grad.detach()),
        loaded_energy_grad=tuple(float(v) for v in loaded_e.grad.detach()),
        event_edges=tuple(meta),
        event_edge_grad=edge_grad,
        completion_nodes=tuple(int(v) for v in completion_nodes.tolist()),
        surrogate_grad=surrogate_feature_gradients(model, schedule, instance) if model is not None else None,
    )


def explain_schedules(
    schedules: list[Schedule], instance: Instance, model: nn.Module | None = None
) -> list[TapeExplanation]:
    """Run TAPE on a Pareto set or final-generation schedule list."""
    return [explain_schedule(s, instance, model) for s in schedules]


def surrogate_feature_gradients(model: nn.Module, schedule: Schedule, instance: Instance) -> dict[str, Any]:
    """Frozen E-HGATv2 input-feature gradients (model-faithfulness, not the TAPE oracle)."""
    for p in model.parameters():
        p.requires_grad_(False)
    model.eval()
    data = build_hetero_graph(schedule, instance)
    data[NODE_TYPE].x.requires_grad_(True)
    data[AGV_EDGE].edge_attr.requires_grad_(True)
    data[QC_EDGE].edge_attr.requires_grad_(True)
    out, _ = model(data)
    pred = out * model.target_std + model.target_mean  # physical units
    pred[0, 0].backward(retain_graph=True)
    c_node = data[NODE_TYPE].x.grad.detach().clone()
    c_agv = data[AGV_EDGE].edge_attr.grad.detach().clone()
    data[NODE_TYPE].x.grad.zero_(); data[AGV_EDGE].edge_attr.grad.zero_()
    if data[QC_EDGE].edge_attr.grad is not None:
        data[QC_EDGE].edge_attr.grad.zero_()
    pred[0, 1].backward()
    return {
        "makespan_node_grad": c_node.tolist(),
        "makespan_agv_edge_grad": c_agv.tolist(),
        "energy_node_grad": data[NODE_TYPE].x.grad.detach().tolist(),
        "energy_agv_edge_grad": data[AGV_EDGE].edge_attr.grad.detach().tolist(),
    }
