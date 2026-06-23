"""Fused-GNN TAPE guidance signals for the attention-guided NSGA-II (Signal #3).

This is the *faithful* alternative to the bare-attention readout used by
:func:`~ehgat.search.attention_nsga2.attention_task_probabilities` /
:func:`~ehgat.search.attention_nsga2._attention_signals`. Instead of the learned (and
empirically near-random) HAN attention weights, the guidance signal here is the fused
model's **native TAPE**: ``dC_max/d(leg time)`` and ``dC_max/d(tau)`` extracted from the
differentiable max-plus DP head (:func:`~ehgat.explain.fused_explainer.explain_fused`).

Because ``C_max`` is routed through the exact tropical longest path, these gradients are
**binary critical-path indicators** -- faithful by construction. Routing them through the
search means the *same* signal that explains a schedule (Req 2) also steers the mutation
(Req 3): one evidenced mechanism for both requirements.

Crucially the GNN stays load-bearing. The critical path is read off the GNN's *own
predicted* leg physics (the heads map graph structure -> leg times / delays / coupled
waits); TAPE only makes that prediction faithfully inspectable. This is NOT the exact
deterministic critical path (``critical_path_binding``), which uses no GNN and is kept
only as a ceiling baseline.

The outputs deliberately mirror the attention path's ``(task_probs, w_agv, w_qc)`` triple
so they drop straight into the existing ``signals`` plumbing of ``_mutate``:

* ``w_agv[j]`` -- AGV-leg criticality of task ``j`` = ``dC_max/d(empty_t_j) +
  dC_max/d(loaded_t_j)`` (its incoming AGV arc is on the critical path).
* ``w_qc[j]``  -- QC-handling criticality of task ``j`` = ``dC_max/d(tau_j)`` (its crane
  delay is on the critical path).
* ``task_probs`` -- temperature-softmax over total criticality ``w_agv + w_qc`` (which
  task to mutate), so mutation concentrates on the tasks that actually gate ``C_max``.

The AGV-vs-QC split feeds the Channel-B operator router exactly as the attention weights
do: ``w_agv[j] / (w_agv[j] + w_qc[j])`` is the per-task AGV bias (1.0 => AGV-bound, pick
``reassign``/``swap_agv``; 0.0 => QC-bound, pick ``swap_qc``; 0.5 when off the path).
"""

from __future__ import annotations

import numpy as np
import torch

from ehgat.environment.decoder import Schedule
from ehgat.environment.instance import Instance
from ehgat.explain.fused_ehgat import FusedEHGATv2
from ehgat.explain.fused_explainer import explain_fused
from ehgat.surrogate.graph import build_hetero_graph

__all__ = [
    "tape_predict_objectives",
    "tape_signals",
    "tape_signals_batch",
]

Objectives = tuple[float, float]
_SIGNAL = tuple[np.ndarray, np.ndarray, np.ndarray]


def _softmax_probs(criticality: np.ndarray, temperature: float) -> np.ndarray:
    """Temperature-softmax over per-task criticality (uniform when all-zero/degenerate)."""
    n = criticality.shape[0]
    if n == 0:
        return criticality
    if not np.any(criticality > 0.0):
        return np.full(n, 1.0 / n)
    logits = (criticality - criticality.max()) / max(temperature, 1e-6)
    exp = np.exp(logits)
    return np.asarray(exp / exp.sum())


def tape_signals(
    model: FusedEHGATv2, schedule: Schedule, instance: Instance, temperature: float
) -> _SIGNAL:
    """Fused-GNN TAPE ``(task_probs, w_agv, w_qc)`` for one schedule.

    ``w_agv``/``w_qc`` are the per-task AGV-leg / QC-handling critical-path criticalities
    (``dC_max/d(leg time)`` / ``dC_max/d(tau)``); ``task_probs`` is the temperature-softmax
    over their sum. Mirrors :func:`~ehgat.search.attention_nsga2._attention_signals` so it
    feeds the same ``_mutate`` ``signals`` channel.
    """
    ex = explain_fused(model, schedule, instance)
    empty_g = np.asarray(ex.empty_time_grad, dtype=float)
    loaded_g = np.asarray(ex.loaded_time_grad, dtype=float)
    node_g = np.asarray(ex.node_grad, dtype=float)
    # Gradients are non-negative critical-path indicators; clamp tiny negatives from the
    # tropical subgradient's tie-handling so the bias/softmax stay well-defined.
    w_agv = np.clip(empty_g + loaded_g, 0.0, None)
    w_qc = np.clip(node_g, 0.0, None)
    task_probs = _softmax_probs(w_agv + w_qc, temperature)
    return task_probs, w_agv, w_qc


def tape_signals_batch(
    model: FusedEHGATv2, schedules: list[Schedule], instance: Instance, temperature: float
) -> list[_SIGNAL]:
    """Per-schedule TAPE signals (the tropical DP is assembled per graph, so this loops)."""
    return [tape_signals(model, s, instance, temperature) for s in schedules]


@torch.no_grad()
def tape_predict_objectives(
    model: FusedEHGATv2, schedules: list[Schedule], instance: Instance
) -> list[Objectives]:
    """Fused-model ``(makespan, energy)`` predictions for offspring screening.

    The physics-fused head's near-exact regression pre-filters a ``k*lambda`` candidate
    pool so the expensive exact evaluations are spent only on predicted-dominant offspring
    -- the same role :func:`~ehgat.search.attention_nsga2._predict_objectives` plays for
    the bare core, but using the fused head (which is also what TAPE explains).
    """
    model.eval()
    out: list[Objectives] = []
    for s in schedules:
        pred = model(build_hetero_graph(s, instance))
        out.append((float(pred.makespan.detach()), float(pred.energy.detach())))
    return out
