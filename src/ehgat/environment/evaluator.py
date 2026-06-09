"""Schedule evaluator: makespan ``C_max`` and total AGV energy ``E`` (Module 1).

This is the **physical ground truth** every other component is measured against, so
the timing model is stated explicitly. It operationalises the MILP recurrences of
Homayouni & Fontes (2022) (loading eqs. 1-15, unloading eqs. 16-19) and the
dual-cycling completion/precedence relations.

Per task ``j`` (assigned to one AGV; its QC processes containers one at a time):

- The AGV first drives **empty** from its current position to ``pickup(j)``, then
  **loaded** from ``pickup(j)`` to ``dropoff(j)``.
- **LOAD** (export, yard -> ship): loaded leg ``LU -> QC``. The AGV delivers and is
  immediately free; the QC then lifts the container onto the ship::

      arr_dropoff = agv_ready + empty_time + loaded_time          # delivery to QC
      c_j         = max(arr_dropoff, qc_prev_finish) + tau        # QC completion
      completion  = c_j                                           # Cmax >= c_j

- **UNLOAD** (import, ship -> yard): loaded leg ``QC -> LU``. The QC lifts the
  container onto a *waiting* AGV (so the QC op needs both the QC free and the AGV
  present), then the AGV carries it to the yard::

      arr_pickup  = agv_ready + empty_time                        # AGV reaches QC
      c_j         = max(arr_pickup, qc_prev_finish) + tau         # container on AGV
      arr_dropoff = c_j + loaded_time                             # delivery to yard
      completion  = arr_dropoff                                   # Cmax >= r_j

In both cases the AGV becomes free at ``arr_dropoff`` positioned at ``dropoff(j)``.

``C_max = max_j completion[j]``. Energy ``E = sum_j (empty_energy[j] + loaded_energy[j])``.

Because makespan is a maximum over sums along AGV/QC precedence chains, it is exactly
a **max-plus longest path** over the schedule's precedence DAG -- the physics the
E-HGATv2 surrogate is built to embed. Evaluation processes tasks in a topological
order obtained from Kahn's algorithm over the precedence edges
``{agv_prev -> j, qc_prev -> j}``; if no topological order exists the schedule
contains an AGV/QC deadlock and :class:`ScheduleCycleError` is raised.
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass
from itertools import pairwise

from ehgat.environment.decoder import Schedule
from ehgat.environment.instance import Instance, TaskKind
from ehgat.environment.physics import leg_energy, travel_time

__all__ = ["Evaluation", "ScheduleCycleError", "build_precedence", "evaluate"]


class ScheduleCycleError(ValueError):
    """Raised when AGV and QC precedence chains form a deadlock (no topo order)."""


@dataclass(frozen=True, slots=True)
class Evaluation:
    """Resolved timings, leg costs and objectives for one schedule."""

    makespan: float
    energy: float
    completion: tuple[float, ...]
    qc_finish: tuple[float, ...]
    arr_pickup: tuple[float, ...]
    arr_dropoff: tuple[float, ...]
    agv_free_after: tuple[float, ...]
    empty_time: tuple[float, ...]
    loaded_time: tuple[float, ...]
    empty_energy: tuple[float, ...]
    loaded_energy: tuple[float, ...]
    topo_order: tuple[int, ...]

    @property
    def objectives(self) -> tuple[float, float]:
        """Bi-objective vector ``(C_max, E)`` (both minimised)."""
        return (self.makespan, self.energy)


def _predecessors(sequences: tuple[tuple[int, ...], ...], n: int) -> list[int]:
    """Map ``task_id -> immediate predecessor in its chain`` (or ``-1`` if first)."""
    prev = [-1] * n
    for seq in sequences:
        for earlier, later in pairwise(seq):
            prev[later] = earlier
    return prev


def _topological_order(agv_prev: list[int], qc_prev: list[int], n: int) -> tuple[int, ...]:
    """Kahn's algorithm over ``{agv_prev -> j, qc_prev -> j}`` edges.

    Ties are broken by ascending ``task_id`` (min-heap) for deterministic ordering.
    Raises :class:`ScheduleCycleError` if a topological order does not exist.
    """
    indegree = [0] * n
    successors: list[list[int]] = [[] for _ in range(n)]
    for j in range(n):
        for p in (agv_prev[j], qc_prev[j]):
            if p >= 0:
                successors[p].append(j)
                indegree[j] += 1

    ready = [j for j in range(n) if indegree[j] == 0]
    heapq.heapify(ready)
    order: list[int] = []
    while ready:
        j = heapq.heappop(ready)
        order.append(j)
        for s in successors[j]:
            indegree[s] -= 1
            if indegree[s] == 0:
                heapq.heappush(ready, s)

    if len(order) != n:
        raise ScheduleCycleError(
            f"schedule has an AGV/QC precedence deadlock: only {len(order)}/{n} "
            "tasks could be ordered (a cycle exists in the precedence graph)."
        )
    return tuple(order)


def build_precedence(
    agv_sequences: tuple[tuple[int, ...], ...],
    qc_sequences: tuple[tuple[int, ...], ...],
    n: int,
) -> tuple[list[int], list[int], tuple[int, ...]]:
    """Resolve ``(agv_prev, qc_prev, topo_order)`` for the given chains.

    ``agv_prev[j]``/``qc_prev[j]`` are immediate predecessors (``-1`` if first).
    ``topo_order`` is a deterministic Kahn ordering; raises
    :class:`ScheduleCycleError` on a deadlock. Shared by the evaluator and the oracle.
    """
    agv_prev = _predecessors(agv_sequences, n)
    qc_prev = _predecessors(qc_sequences, n)
    order = _topological_order(agv_prev, qc_prev, n)
    return agv_prev, qc_prev, order


def evaluate(schedule: Schedule, instance: Instance) -> Evaluation:
    """Compute ``(C_max, E)`` and full timings for ``schedule`` on ``instance``."""
    n = instance.num_tasks
    agv_prev, qc_prev, order = build_precedence(
        schedule.agv_sequences, schedule.qc_sequences, n
    )

    completion = [0.0] * n
    qc_finish = [0.0] * n
    arr_pickup = [0.0] * n
    arr_dropoff = [0.0] * n
    agv_free_after = [0.0] * n
    empty_time = [0.0] * n
    loaded_time = [0.0] * n
    empty_energy = [0.0] * n
    loaded_energy = [0.0] * n

    for j in order:
        task = instance.tasks[j]

        ap = agv_prev[j]
        if ap < 0:
            agv_ready = 0.0
            origin = instance.agv_start
        else:
            agv_ready = agv_free_after[ap]
            origin = instance.tasks[ap].dropoff

        empty_dist = instance.distance.distance(origin, task.pickup)
        loaded_dist = instance.loaded_distance(task)
        empty_time[j] = travel_time(empty_dist, schedule.empty_speed[j], loaded=False)
        loaded_time[j] = travel_time(loaded_dist, schedule.loaded_speed[j], loaded=True)
        empty_energy[j] = leg_energy(empty_dist, schedule.empty_speed[j], loaded=False)
        loaded_energy[j] = leg_energy(loaded_dist, schedule.loaded_speed[j], loaded=True)

        qp = qc_prev[j]
        qc_ready = qc_finish[qp] if qp >= 0 else 0.0

        arr_pickup[j] = agv_ready + empty_time[j]
        if task.kind is TaskKind.LOAD:
            # Deliver to the QC first, then the QC loads onto the ship.
            arr_dropoff[j] = arr_pickup[j] + loaded_time[j]
            qc_finish[j] = max(arr_dropoff[j], qc_ready) + task.handling_time
            completion[j] = qc_finish[j]
        else:
            # QC lifts onto the waiting AGV, then the AGV carries it to the yard.
            qc_finish[j] = max(arr_pickup[j], qc_ready) + task.handling_time
            arr_dropoff[j] = qc_finish[j] + loaded_time[j]
            completion[j] = arr_dropoff[j]

        agv_free_after[j] = arr_dropoff[j]

    makespan = max(completion)
    energy = sum(empty_energy) + sum(loaded_energy)

    return Evaluation(
        makespan=makespan,
        energy=energy,
        completion=tuple(completion),
        qc_finish=tuple(qc_finish),
        arr_pickup=tuple(arr_pickup),
        arr_dropoff=tuple(arr_dropoff),
        agv_free_after=tuple(agv_free_after),
        empty_time=tuple(empty_time),
        loaded_time=tuple(loaded_time),
        empty_energy=tuple(empty_energy),
        loaded_energy=tuple(loaded_energy),
        topo_order=order,
    )
