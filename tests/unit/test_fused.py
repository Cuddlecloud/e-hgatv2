"""Tests for the physics-fused E-HGATv2 (tropical makespan + additive energy head)."""

from __future__ import annotations

from ehgat.environment.decoder import NUM_BLOCKS, decode
from ehgat.environment.instance import build_toy_instance
from ehgat.explain.fused_ehgat import FusedEHGATv2
from ehgat.explain.fused_explainer import (
    explain_fused,
    faithfulness_report,
    fused_pareto_tension_scores,
)
from ehgat.surrogate.ehgatv2 import EHGATv2, EHGATv2Config
from ehgat.utils.seeding import make_rng


def _fresh_model() -> FusedEHGATv2:
    core = EHGATv2(EHGATv2Config(hidden=32, layers=2, heads=4))
    model = FusedEHGATv2(core)
    model.freeze_core()
    return model


def _is_integer(value: float, tol: float = 1e-6) -> bool:
    return abs(value - round(value)) < tol


def test_fused_makespan_gradients_are_binary_critical_path() -> None:
    inst = build_toy_instance(num_tasks=6)
    schedule = decode(make_rng(0).random(NUM_BLOCKS * inst.num_tasks), inst)
    ex = explain_fused(_fresh_model(), schedule, inst)

    # The tropical DP head routes the makespan subgradient only along the critical path,
    # so leg/arc gradients are exact integers (no smearing) regardless of head weights.
    for g in ex.empty_time_grad + ex.loaded_time_grad:
        assert _is_integer(g) and g >= 0.0
    assert max(ex.event_edge_grad) == 1.0
    assert max(ex.empty_time_grad + ex.loaded_time_grad) >= 1.0

    # The additive energy head is strictly linear: dE/d(leg energy) == 1 everywhere.
    assert all(abs(g - 1.0) < 1e-6 for g in ex.empty_energy_grad)
    assert all(abs(g - 1.0) < 1e-6 for g in ex.loaded_energy_grad)


def test_fused_pts_is_json_shaped() -> None:
    inst = build_toy_instance(num_tasks=4)
    rng = make_rng(1)
    schedules = [decode(rng.random(NUM_BLOCKS * inst.num_tasks), inst) for _ in range(3)]
    out = fused_pareto_tension_scores(_fresh_model(), schedules, inst)
    assert len(out) == 3
    assert "lambda" in out[0]
    assert out[0]["tasks"]
    assert out[0]["event_arcs"]


def test_fused_objectives_are_finite_and_positive() -> None:
    from ehgat.surrogate.graph import build_hetero_graph

    inst = build_toy_instance(num_tasks=5)
    schedule = decode(make_rng(2).random(NUM_BLOCKS * inst.num_tasks), inst)
    out = _fresh_model()(build_hetero_graph(schedule, inst))
    assert float(out.makespan) > 0.0
    assert float(out.energy) > 0.0


def test_fused_training_recovers_physics_and_is_faithful() -> None:
    # Integration test: after anchoring, the fused model snaps onto the physics
    # (high R^2) and its native critical path agrees with the exact TAPE oracle.
    from ehgat.explain.train_fused import FusedTrainConfig, build_core, train_fused

    inst = build_toy_instance(num_tasks=6)
    core = build_core(inst, seed=0, num_samples=600, epochs=40)
    result = train_fused(inst, core, FusedTrainConfig(num_samples=300, epochs=25, seed=0))

    assert result.metrics["r2_makespan"] >= 0.9
    assert result.metrics["r2_energy"] >= 0.95

    rng = make_rng(99)
    schedule = decode(rng.random(NUM_BLOCKS * inst.num_tasks), inst)
    report = faithfulness_report(result.model, schedule, inst)
    assert report.leg_critical_jaccard >= 0.5
