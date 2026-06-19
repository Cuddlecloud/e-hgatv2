"""Batched fused forward must equal the per-graph fused forward for the same weights."""

from __future__ import annotations

import torch

from ehgat.environment.instance import build_toy_instance
from ehgat.explain.fused_ehgat import FusedEHGATv2
from ehgat.explain.train_fused import build_core, build_samples
from ehgat.explain.train_fused_batched import _forward_batch, build_batch, train_fused_batched
from ehgat.explain.train_fused import FusedTrainConfig


def test_batched_forward_matches_per_graph() -> None:
    inst = build_toy_instance(num_tasks=6, peak_power=30.0)
    core = build_core(inst, seed=0, num_samples=250, epochs=5)
    model = FusedEHGATv2(core, coupled=True)
    model.freeze_core()
    samples = build_samples(inst, 12, seed=1)

    b = build_batch(model, samples, inst)
    _, _, _, mk, en = _forward_batch(model, b, coupled=True)

    for i, s in enumerate(samples):
        out = model(s.data)
        assert abs(float(out.makespan) - float(mk[i])) < 1e-4, f"makespan mismatch @ {i}"
        # Energy ~ O(1e4); float32 summation order differs negligibly -> relative tolerance.
        assert abs(float(out.energy) - float(en[i])) <= 1e-4 * abs(float(en[i])), f"energy @ {i}"


def test_batched_training_runs_and_fits_energy() -> None:
    inst = build_toy_instance(num_tasks=6, peak_power=30.0)
    core = build_core(inst, seed=0, num_samples=400, epochs=20)
    res = train_fused_batched(
        inst, core, FusedTrainConfig(num_samples=300, epochs=40, seed=0), device="cpu"
    )
    # Energy is exact-additive; makespan should be a sensible positive fit.
    assert res.metrics["r2_energy"] >= 0.98
    assert res.metrics["r2_makespan"] >= 0.5
