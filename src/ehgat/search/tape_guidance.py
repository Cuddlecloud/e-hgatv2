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
from ehgat.explain.fused_explainer import explain_fused, explain_fused_batch
from ehgat.explain.tape_explainer import TapeExplanation
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


def _signal_from_explanation(ex: TapeExplanation, temperature: float) -> _SIGNAL:
    """Turn one TAPE explanation into the ``(task_probs, w_agv, w_qc)`` guidance signal."""
    empty_g = np.asarray(ex.empty_time_grad, dtype=float)
    loaded_g = np.asarray(ex.loaded_time_grad, dtype=float)
    node_g = np.asarray(ex.node_grad, dtype=float)
    # Gradients are non-negative critical-path indicators; clamp tiny negatives from the
    # tropical subgradient's tie-handling so the bias/softmax stay well-defined.
    w_agv = np.clip(empty_g + loaded_g, 0.0, None)
    w_qc = np.clip(node_g, 0.0, None)
    task_probs = _softmax_probs(w_agv + w_qc, temperature)
    return task_probs, w_agv, w_qc


def tape_signals(
    model: FusedEHGATv2, schedule: Schedule, instance: Instance, temperature: float
) -> _SIGNAL:
    """Fused-GNN TAPE ``(task_probs, w_agv, w_qc)`` for one schedule.

    ``w_agv``/``w_qc`` are the per-task AGV-leg / QC-handling critical-path criticalities
    (``dC_max/d(leg time)`` / ``dC_max/d(tau)``); ``task_probs`` is the temperature-softmax
    over their sum. Mirrors :func:`~ehgat.search.attention_nsga2._attention_signals` so it
    feeds the same ``_mutate`` ``signals`` channel.
    """
    return _signal_from_explanation(explain_fused(model, schedule, instance), temperature)


def _tape_signals_pergraph(
    model: FusedEHGATv2, schedules: list[Schedule], instance: Instance, temperature: float
) -> list[_SIGNAL]:
    """Per-graph reference: batched encode, then a per-graph fused forward + summed backward
    (see :func:`~ehgat.explain.fused_explainer.explain_fused_batch`). Correct, but the per-node
    ``.item()`` DP loop dominates once screening is batched. Kept as the guidance parity oracle
    (``tests/unit/test_screening_batched_parity.py``); :func:`tape_signals_batch` batches it."""
    if not schedules:
        return []
    return [_signal_from_explanation(ex, temperature)
            for ex in explain_fused_batch(model, schedules, instance)]


def _batched_makespan_grads(
    model: FusedEHGATv2, schedules: list[Schedule], instance: Instance,
    *, chunk_size: int = 128,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Per-task ``dC_max/d(empty_t)``, ``dC_max/d(loaded_t)``, ``dC_max/d(tau)`` for many
    schedules via ONE batched max-plus DP per chunk.

    The schedules stack into a **block-diagonal** batch, so ``sum_i C_max^{(i)}`` has gradient
    ``dC_max^{(i)}/d(leg_i)`` w.r.t. graph ``i``'s legs with no cross terms (the components are
    disjoint) -- each graph's exact binary critical-path subgradient, identical to a per-graph
    :func:`~ehgat.explain.fused_explainer.explain_fused` backward, but the DP is
    :func:`~ehgat.explain.tropical_dp_batched.batched_longest_path` (layer-vectorised, no
    per-node ``.item()`` loop). Returns three ``[T]`` arrays in sample-major task order.
    """
    from ehgat.explain.train_fused import FusedSample
    from ehgat.explain.train_fused_batched import _forward_batch, build_batch

    n = instance.num_tasks
    coupled = instance.peak_power is not None
    dev = next(model.parameters()).device
    model.eval()
    e_out: list[np.ndarray] = []
    l_out: list[np.ndarray] = []
    t_out: list[np.ndarray] = []
    for start in range(0, len(schedules), chunk_size):
        chunk = schedules[start:start + chunk_size]
        samples = [
            FusedSample(
                data=build_hetero_graph(s, instance).to(dev),
                legs=torch.zeros(n, 4), tau=torch.zeros(n),
                objectives=torch.zeros(2), waits=torch.zeros(n, 2),
            )
            for s in chunk
        ]
        b = build_batch(model, samples, instance)
        _batched_to_device(b, dev)
        times, tau, _w, makespan, _e, _s = _forward_batch(model, b, coupled)
        times.retain_grad()
        tau.retain_grad()
        model.zero_grad(set_to_none=True)
        makespan.sum().backward()
        e_out.append(times.grad[:, 0].detach().cpu().numpy())
        l_out.append(times.grad[:, 1].detach().cpu().numpy())
        t_out.append(tau.grad.detach().cpu().numpy())
    return np.concatenate(e_out), np.concatenate(l_out), np.concatenate(t_out)


def tape_signals_batch(
    model: FusedEHGATv2, schedules: list[Schedule], instance: Instance, temperature: float
) -> list[_SIGNAL]:
    """TAPE ``(task_probs, w_agv, w_qc)`` guidance for many schedules via ONE batched max-plus
    DP per chunk (:func:`_batched_makespan_grads`) instead of the per-graph ``.item()`` DP loop
    -- the guidance path is ~59% of the guided search once screening is batched. Same signal as
    looping :func:`tape_signals` (parity-tested); ``w_agv`` = AGV-leg criticality
    ``dC_max/d(empty_t)+dC_max/d(loaded_t)``, ``w_qc`` = QC criticality ``dC_max/d(tau)``.
    """
    if not schedules:
        return []
    n = instance.num_tasks
    empty_g, loaded_g, tau_g = _batched_makespan_grads(model, schedules, instance)
    signals: list[_SIGNAL] = []
    for i in range(len(schedules)):
        sl = slice(i * n, (i + 1) * n)
        w_agv = np.clip((empty_g[sl] + loaded_g[sl]).astype(float), 0.0, None)
        w_qc = np.clip(tau_g[sl].astype(float), 0.0, None)
        task_probs = _softmax_probs(w_agv + w_qc, temperature)
        signals.append((task_probs, w_agv, w_qc))
    return signals


@torch.no_grad()
def _tape_predict_pergraph(
    model: FusedEHGATv2, schedules: list[Schedule], instance: Instance
) -> list[Objectives]:
    """Per-graph reference for offspring screening (kept as the parity oracle).

    Batches only the frozen-core encode, then runs the fused head + tropical DP **one graph
    at a time** -- correct, but the per-node ``.item()`` DP loop dominates wall-clock (68-83%
    of the guided search; see ``tests/unit/test_screening_batched_parity.py``). The public
    :func:`tape_predict_objectives` produces the identical result via one batched max-plus DP.
    """
    from torch_geometric.data import Batch

    from ehgat.surrogate.graph import NODE_TYPE

    model.eval()
    out: list[Objectives] = []
    chunk_size = 256
    for start in range(0, len(schedules), chunk_size):
        chunk = schedules[start:start + chunk_size]
        graphs = [build_hetero_graph(s, instance) for s in chunk]
        batch = Batch.from_data_list(graphs).to(next(model.parameters()).device)
        h_all = model.core.encode(batch)                # ONE batched encode for the chunk
        ptr = batch[NODE_TYPE].ptr.tolist()
        for i, g in enumerate(graphs):
            pred = model(g.to(batch[NODE_TYPE].x.device), h=h_all[ptr[i]:ptr[i + 1]])
            out.append((float(pred.makespan.detach()), float(pred.energy.detach())))
    return out


def _batched_to_device(b, dev) -> None:
    """Move a :class:`BatchedFused`'s forward tensors onto ``dev`` (training targets unused
    for screening). Mirrors the private ``_to`` in :mod:`ehgat.explain.train_fused_batched`."""
    from ehgat.explain.tropical_dp_batched import BatchSchedule

    b.leg_in = b.leg_in.to(dev); b.delay_in = b.delay_in.to(dev)
    b.empty_e = b.empty_e.to(dev); b.loaded_e = b.loaded_e.to(dev)
    b.idx_all = b.idx_all.to(dev); b.edge_weights = b.edge_weights.to(dev)
    b.comp_nodes = b.comp_nodes.to(dev); b.comp_batch = b.comp_batch.to(dev)
    b.task_batch = b.task_batch.to(dev)
    b.schedule = BatchSchedule(
        edge_index=b.schedule.edge_index.to(dev), num_nodes=b.schedule.num_nodes,
        layers=tuple((a.to(dev), c.to(dev), d.to(dev)) for a, c, d in b.schedule.layers),
    )


@torch.no_grad()
def tape_predict_objectives(
    model: FusedEHGATv2, schedules: list[Schedule], instance: Instance,
    *, chunk_size: int = 256,
) -> list[Objectives]:
    """Fused-model ``(makespan, energy)`` predictions for offspring screening.

    The physics-fused head's near-exact regression pre-filters a ``k*lambda`` candidate
    pool so the expensive exact evaluations are spent only on predicted-dominant offspring
    -- the same role :func:`~ehgat.search.attention_nsga2._predict_objectives` plays for
    the bare core, but using the fused head (which is also what TAPE explains).

    Computes every candidate's makespan with **one** vectorised max-plus DP per chunk
    (:func:`~ehgat.explain.tropical_dp_batched.batched_longest_path`) over a block-diagonal
    batch, instead of the per-graph ``.item()`` DP loop that otherwise dominates the search.
    Bit-identical to :func:`_tape_predict_pergraph` (parity-tested), both regimes.
    """
    if not schedules:
        return []
    from ehgat.explain.train_fused import FusedSample
    from ehgat.explain.train_fused_batched import _forward_batch, build_batch

    n = instance.num_tasks
    coupled = instance.peak_power is not None
    dev = next(model.parameters()).device
    model.eval()
    out: list[Objectives] = []
    for start in range(0, len(schedules), chunk_size):
        chunk = schedules[start:start + chunk_size]
        # Dummy targets: build_batch only reads ``data`` (encode + head features) and the
        # precedence structure for the forward; legs/tau/waits/objectives are training labels.
        samples = [
            FusedSample(
                data=build_hetero_graph(s, instance).to(dev),
                legs=torch.zeros(n, 4), tau=torch.zeros(n),
                objectives=torch.zeros(2), waits=torch.zeros(n, 2),
            )
            for s in chunk
        ]
        b = build_batch(model, samples, instance)
        _batched_to_device(b, dev)
        _, _, _, makespan, energy, _ = _forward_batch(model, b, coupled)
        out.extend(
            (float(m), float(e)) for m, e in zip(makespan.tolist(), energy.tolist())
        )
    return out
