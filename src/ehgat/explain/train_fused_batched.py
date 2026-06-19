"""Batched fine-tuning of the fused tropical head (GPU-ready, structure cached once).

The per-graph :func:`~ehgat.explain.train_fused.train_fused` loops Python over every sample
*and* every node of its DAG, every epoch -- the dominant cost at scale. This module computes
the **identical** physics-fused objectives, but vectorised over the whole dataset:

- the frozen-core embeddings and all head-input features are computed **once** (the core is
  frozen, so they never change);
- all samples are stacked into one **block-diagonal** coupled activity DAG, whose structure
  (edges, ranks, node<->leg index map) is built **once**;
- each epoch runs the heads on the stacked features in a single matmul, scatters the predicted
  leg/wait/tau values into the batched node weights, and computes every sample's makespan with
  ONE :func:`~ehgat.explain.tropical_dp_batched.batched_longest_path` call.

The Python loop length per epoch drops from ``sum_k (N_k + E_k)`` to ``max_k depth_k``, and the
whole step is tensor ops that run on GPU. Results match the per-graph path (same heads, same
max-plus semantics); see ``tests/unit/test_fused_batched.py``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import torch
from torch import Tensor

from ehgat.environment.instance import Instance
from ehgat.explain.event_dag import assemble_coupled_event_dag, extract_precedence
from ehgat.explain.fused_ehgat import FusedEHGATv2
from ehgat.explain.train_fused import (
    FusedSample,
    FusedTrainConfig,
    FusedTrainResult,
    _scales,
    build_samples,
)
from ehgat.surrogate.ehgatv2 import EHGATv2
from ehgat.surrogate.graph import AGV_EDGE, NODE_TYPE, QC_EDGE
from ehgat.explain.tropical_dp_batched import BatchSchedule, batched_longest_path, build_batch_schedule
from ehgat.explain.train_fused import build_core
from ehgat.utils.seeding import make_rng, seed_everything

__all__ = ["BatchedFused", "build_batch", "train_fused_batched"]


@dataclass
class BatchedFused:
    """Pre-assembled, structure-cached batch of fused samples (all static tensors)."""

    leg_in: Tensor          # [T, 2H+EDGE_DIM] leg/wait head input
    delay_in: Tensor        # [T, H+1] tau head input
    empty_e: Tensor         # [T]
    loaded_e: Tensor        # [T]
    idx_all: Tensor         # [3T] node positions for (empty, loaded, tau) scatter
    schedule: BatchSchedule
    edge_weights: Tensor    # [E] zeros (coupled DAG carries weight on nodes)
    num_nodes: int
    comp_nodes: Tensor      # [S*?] completion node global ids
    comp_batch: Tensor      # [same] sample id per completion node
    task_batch: Tensor      # [T] sample id per task (for energy segment-sum)
    num_samples: int
    # targets
    leg_true: Tensor        # [T, 2]
    tau_true: Tensor        # [T]
    wait_true: Tensor       # [T, 2]
    mk_true: Tensor         # [S]
    energy_true: Tensor     # [S]


def build_batch(model: FusedEHGATv2, samples: list[FusedSample], instance: Instance) -> BatchedFused:
    """Assemble the block-diagonal batch + cached structure for ``samples`` (once)."""
    n = instance.num_tasks
    leg_in_l, delay_in_l, empty_e_l, loaded_e_l = [], [], [], []
    idx_empty_l, idx_loaded_l, idx_tau_l = [], [], []
    edge_src_l, edge_dst_l = [], []
    comp_nodes_l, comp_batch_l, task_batch_l = [], [], []
    leg_true_l, tau_true_l, wait_true_l, mk_true_l, e_true_l = [], [], [], [], []

    node_off = 0
    for s_i, s in enumerate(samples):
        data = s.data
        h = model.encode_cached(data)
        leg_in, delay_in, empty_e, loaded_e, _arc = model.static_features(data, h)
        leg_in_l.append(leg_in); delay_in_l.append(delay_in)
        empty_e_l.append(empty_e); loaded_e_l.append(loaded_e)

        is_load = data[NODE_TYPE].x[:, 1] > 0.5
        agv_prev, qc_prev = extract_precedence(
            data[AGV_EDGE].edge_index, data[QC_EDGE].edge_index, n
        )
        # Structure only (arc-free, matching the per-graph fused forward: predicted per-leg
        # waits absorb the power delays). Reuse the assembler with the TRUE legs just to grab
        # the edge structure + completion nodes.
        dag = assemble_coupled_event_dag(
            is_load, agv_prev, qc_prev, s.legs[:, 0], s.legs[:, 1], s.tau, []
        )
        edge_src_l.append(dag.edge_index[0] + node_off)
        edge_dst_l.append(dag.edge_index[1] + node_off)
        comp_nodes_l.append(dag.completion_nodes + node_off)
        comp_batch_l.append(torch.full((n,), s_i, dtype=torch.long))
        task_batch_l.append(torch.full((n,), s_i, dtype=torch.long))

        base = node_off + 1  # node 0 of this sample is its source
        j = torch.arange(n, dtype=torch.long)
        idx_empty_l.append(base + 3 * j)
        idx_loaded_l.append(base + 3 * j + 2)
        idx_tau_l.append(base + 3 * j + 1)

        leg_true_l.append(s.legs[:, :2]); tau_true_l.append(s.tau); wait_true_l.append(s.waits)
        mk_true_l.append(s.objectives[0]); e_true_l.append(s.objectives[1])
        node_off += 1 + 3 * n

    edge_index = torch.stack([torch.cat(edge_src_l), torch.cat(edge_dst_l)], dim=0)
    idx_all = torch.cat(idx_empty_l + idx_loaded_l + idx_tau_l)
    schedule = build_batch_schedule(edge_index, node_off)
    return BatchedFused(
        leg_in=torch.cat(leg_in_l), delay_in=torch.cat(delay_in_l),
        empty_e=torch.cat(empty_e_l), loaded_e=torch.cat(loaded_e_l),
        idx_all=idx_all, schedule=schedule,
        edge_weights=torch.zeros(edge_index.shape[1]), num_nodes=node_off,
        comp_nodes=torch.cat(comp_nodes_l), comp_batch=torch.cat(comp_batch_l),
        task_batch=torch.cat(task_batch_l), num_samples=len(samples),
        leg_true=torch.cat(leg_true_l), tau_true=torch.cat(tau_true_l),
        wait_true=torch.cat(wait_true_l),
        mk_true=torch.stack(mk_true_l), energy_true=torch.stack(e_true_l),
    )


_NEG_INF = -1.0e30


def _forward_batch(model: FusedEHGATv2, b: BatchedFused, coupled: bool) -> tuple[Tensor, Tensor, Tensor, Tensor, Tensor]:
    """Vectorised fused forward over the whole batch -> (times, tau, waits, makespan, energy)."""
    times = (model.leg_head(b.leg_in) * model.leg_std + model.leg_mean).clamp_min(0.0)
    tau = (model.delay_head(b.delay_in).squeeze(-1) * model.tau_std + model.tau_mean).clamp_min(0.0)
    if coupled:
        waits = (model.wait_head(b.leg_in) * model.wait_std + model.wait_mean).clamp_min(0.0)
    else:
        waits = torch.zeros_like(times)
    empty_eff = times[:, 0] + waits[:, 0]
    loaded_eff = times[:, 1] + waits[:, 1]
    vals_all = torch.cat([empty_eff, loaded_eff, tau])
    node_weights = torch.zeros(b.num_nodes, dtype=times.dtype, device=times.device).index_add(
        0, b.idx_all, vals_all
    )
    x = batched_longest_path(node_weights, b.edge_weights, b.schedule)
    comp_vals = x[b.comp_nodes]
    makespan = torch.full((b.num_samples,), _NEG_INF, dtype=x.dtype, device=x.device)
    makespan = makespan.scatter_reduce(0, b.comp_batch, comp_vals, reduce="amax", include_self=True)
    leg_e = b.empty_e + b.loaded_e
    energy = torch.zeros(b.num_samples, dtype=x.dtype, device=x.device).index_add(0, b.task_batch, leg_e)
    return times, tau, waits, makespan, energy


def _r2(pred: Tensor, true: Tensor) -> float:
    ss_res = torch.sum((true - pred) ** 2)
    ss_tot = torch.sum((true - true.mean()) ** 2).clamp_min(1e-12)
    return float(1.0 - ss_res / ss_tot)


def train_fused_batched(
    instance: Instance,
    core: EHGATv2 | None = None,
    config: FusedTrainConfig | None = None,
    *,
    device: str = "cpu",
) -> FusedTrainResult:
    """Batched equivalent of :func:`train_fused` (same loss/semantics, vectorised + GPU-ready)."""
    config = config or FusedTrainConfig()
    seed_everything(config.seed)
    if core is None:
        core = build_core(instance, seed=config.seed)

    coupled = instance.peak_power is not None
    model = FusedEHGATv2(core, use_physics_prior=config.use_physics_prior, coupled=coupled)
    model.freeze_core()

    samples = build_samples(instance, config.num_samples, seed=config.seed)
    rng = make_rng(config.seed)
    order = rng.permutation(len(samples)).tolist()
    samples = [samples[i] for i in order]
    n_val = round(config.val_frac * len(samples))
    val_samples, train_samples = samples[:n_val], samples[n_val:]
    scales = _scales(train_samples)

    tr_times = torch.cat([s.legs[:, :2] for s in train_samples], dim=0)
    tr_tau = torch.cat([s.tau for s in train_samples], dim=0)
    tr_w = torch.cat([s.waits for s in train_samples], dim=0)
    model.set_leg_normalization(
        leg_mean=tr_times.mean(0), leg_std=tr_times.std(0),
        tau_mean=tr_tau.mean(), tau_std=tr_tau.std(),
        wait_mean=tr_w.mean(0), wait_std=tr_w.std(0),
    )

    # Build the batch (frozen-core encode + static features) while everything is on CPU,
    # THEN move the model and the batched tensors to the target device.
    train_b = build_batch(model, train_samples, instance)
    val_b = build_batch(model, val_samples, instance) if val_samples else None
    dev = torch.device(device)
    model = model.to(dev)

    def _to(b: BatchedFused) -> None:
        b.leg_in = b.leg_in.to(dev); b.delay_in = b.delay_in.to(dev)
        b.empty_e = b.empty_e.to(dev); b.loaded_e = b.loaded_e.to(dev)
        b.idx_all = b.idx_all.to(dev); b.edge_weights = b.edge_weights.to(dev)
        b.comp_nodes = b.comp_nodes.to(dev); b.comp_batch = b.comp_batch.to(dev)
        b.task_batch = b.task_batch.to(dev)
        b.leg_true = b.leg_true.to(dev); b.tau_true = b.tau_true.to(dev)
        b.wait_true = b.wait_true.to(dev); b.mk_true = b.mk_true.to(dev)
        b.schedule = BatchSchedule(
            edge_index=b.schedule.edge_index.to(dev), num_nodes=b.schedule.num_nodes,
            layers=tuple((a.to(dev), c.to(dev), d.to(dev)) for a, c, d in b.schedule.layers),
        )
    _to(train_b)
    if val_b is not None:
        _to(val_b)
    s_leg = scales["leg"].to(dev); s_tau = scales["tau"].to(dev)
    s_w = scales["wait"].to(dev); s_mk = scales["makespan"].to(dev); s_e = scales["energy"].to(dev)

    opt = torch.optim.Adam(model.head_parameters(), lr=config.lr, weight_decay=config.weight_decay)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=config.epochs, eta_min=config.eta_min)

    result = FusedTrainResult(model=model)
    for epoch in range(config.epochs):
        model.train(); model.core.eval()
        opt.zero_grad()
        times, tau, waits, makespan, energy = _forward_batch(model, train_b, coupled)
        leg_term = (((times - train_b.leg_true) / s_leg) ** 2).mean()
        tau_term = (((tau - train_b.tau_true) / s_tau) ** 2).mean()
        cmax_term = (((makespan - train_b.mk_true) / s_mk) ** 2).mean()
        e_term = (((energy - train_b.energy_true.to(dev)) / s_e) ** 2).mean()
        loss = leg_term + tau_term + config.alpha_makespan * cmax_term + config.beta_energy * e_term
        if coupled:
            loss = loss + (((waits - train_b.wait_true) / s_w) ** 2).mean()
        loss.backward(); opt.step(); sched.step()

        record = {"epoch": float(epoch), "train_loss": float(loss)}
        if val_b is not None:
            with torch.no_grad():
                model.eval()
                _, _, _, vmk, ven = _forward_batch(model, val_b, coupled)
                record["r2_makespan"] = _r2(vmk, val_b.mk_true)
                record["r2_energy"] = _r2(ven, val_b.energy_true.to(dev))
        result.history.append(record)

    eb = val_b if val_b is not None else train_b
    with torch.no_grad():
        model.eval()
        _, _, _, mk, en = _forward_batch(model, eb, coupled)
        result.metrics = {
            "r2_makespan": _r2(mk, eb.mk_true),
            "r2_energy": _r2(en, eb.energy_true.to(dev)),
            "mae_makespan": float((mk - eb.mk_true).abs().mean()),
        }
    model = model.to("cpu")
    return result
