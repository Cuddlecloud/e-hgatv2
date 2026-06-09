"""Tests for the attention-guided NSGA-II (Module 4, ``search/attention_nsga2.py``).

The headline guarantees: (1) the **no-deadlock invariant** -- the direct AGV-sequence
swap operator can create an AGV/QC cycle but is always Kahn-re-validated, so every
schedule admitted to the population is acyclic; (2) **Oracle-bound soundness** -- because
objectives come from the exact evaluator, every front point is weakly dominated by the
golden ``PF*``; plus determinism, evaluation accounting and a non-dominated front.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("torch_geometric")

from ehgat.environment.decoder import NUM_BLOCKS, decode  # noqa: E402
from ehgat.environment.evaluator import build_precedence, evaluate  # noqa: E402
from ehgat.environment.instance import EXACT_TOY_TASKS, build_toy_instance  # noqa: E402
from ehgat.search.attention_nsga2 import (  # noqa: E402
    AttentionNSGA2Config,
    attention_bottleneck_task,
    default_config,
    mutate_reassign_agv,
    mutate_speed,
    mutate_swap_on_agv,
    run_attention_nsga2,
)
from ehgat.surrogate.train import TrainConfig, train_surrogate  # noqa: E402
from ehgat.utils.seeding import make_rng  # noqa: E402

pytestmark = pytest.mark.learn

GOLDEN_FRONT_N5 = Path(__file__).resolve().parents[1] / "data" / "golden" / "exact_front_n5.json"


def _golden_front() -> list[tuple[float, float]]:
    return [tuple(p) for p in json.loads(GOLDEN_FRONT_N5.read_text())["front"]]


def _instance():
    return build_toy_instance(num_tasks=EXACT_TOY_TASKS)


@pytest.fixture(scope="module")
def trained_model():
    inst = _instance()
    return train_surrogate(inst, TrainConfig(num_samples=400, epochs=10, seed=0)).model


def _deadlock_prone_schedule(inst):
    """A schedule where tasks 0 and 3 (both QC1) sit adjacently on one AGV.

    Swapping them on the AGV contradicts the QC1 order -> an AGV/QC deadlock.
    """
    n = inst.num_tasks
    keys = np.empty(NUM_BLOCKS * n)
    keys[0:n] = [0.1, 0.3, 0.5, 0.7, 0.9]  # global order = identity
    keys[n : 2 * n] = [0.1, 0.9, 0.9, 0.1, 0.9]  # AGV0 = {0, 3}; AGV1 = {1, 2, 4}
    keys[2 * n :] = 0.5  # arbitrary valid speeds
    return decode(keys, inst)


# --------------------------------------------------------------------------------------
# Mutation operators
# --------------------------------------------------------------------------------------
def test_mutate_speed_changes_only_target_speed() -> None:
    inst = _instance()
    sched = decode(make_rng(0).random(NUM_BLOCKS * inst.num_tasks), inst)
    rng = make_rng(1)
    mutated = mutate_speed(sched, task=2, rng=rng)
    changed = sum(
        (mutated.empty_speed[t] != sched.empty_speed[t])
        or (mutated.loaded_speed[t] != sched.loaded_speed[t])
        for t in range(inst.num_tasks)
    )
    assert changed == 1  # exactly the target task's speed changed
    evaluate(mutated, inst)  # still feasible


def test_mutate_reassign_changes_agv_and_stays_acyclic() -> None:
    inst = _instance()
    sched = decode(make_rng(2).random(NUM_BLOCKS * inst.num_tasks), inst)
    mutated = mutate_reassign_agv(sched, inst, task=1, rng=make_rng(3))
    assert mutated.assignment[1] != sched.assignment[1]
    evaluate(mutated, inst)  # re-projection keeps it acyclic


def test_swap_rejects_deadlock_returns_none() -> None:
    inst = _instance()
    sched = _deadlock_prone_schedule(inst)
    # Sanity: 0 and 3 are adjacent on the same AGV and share QC1.
    assert sched.assignment[0] == sched.assignment[3]
    # Swapping task 3 with its AGV predecessor (task 0) must deadlock -> None.
    assert mutate_swap_on_agv(sched, inst, task=3) is None
    # Task at sequence head has no predecessor -> None.
    assert mutate_swap_on_agv(sched, inst, task=0) is None


def test_swap_no_deadlock_invariant_property() -> None:
    """Over many schedules x tasks, every non-None swap result is acyclic."""
    inst = _instance()
    n = inst.num_tasks
    for seed in range(60):
        sched = decode(make_rng(seed).random(NUM_BLOCKS * n), inst)
        for task in range(n):
            mutated = mutate_swap_on_agv(sched, inst, task)
            if mutated is None:
                continue
            # Admitted schedules MUST have a valid topological order (no deadlock).
            build_precedence(mutated.agv_sequences, mutated.qc_sequences, n)
            evaluate(mutated, inst)


# --------------------------------------------------------------------------------------
# Attention bottleneck + full search
# --------------------------------------------------------------------------------------
def test_bottleneck_task_is_valid(trained_model) -> None:
    inst = _instance()
    sched = decode(make_rng(5).random(NUM_BLOCKS * inst.num_tasks), inst)
    task = attention_bottleneck_task(sched, inst, trained_model)
    assert 0 <= task < inst.num_tasks


def test_run_is_deterministic(trained_model) -> None:
    inst = _instance()
    cfg = AttentionNSGA2Config(pop_size=20, generations=8, seed=7)
    a = run_attention_nsga2(inst, trained_model, cfg)
    b = run_attention_nsga2(inst, trained_model, cfg)
    assert a.front == b.front
    assert a.evaluations == b.evaluations
    assert a.deadlocks_rejected == b.deadlocks_rejected


def test_evaluation_accounting(trained_model) -> None:
    inst = _instance()
    cfg = AttentionNSGA2Config(pop_size=20, generations=8, seed=0)
    res = run_attention_nsga2(inst, trained_model, cfg)
    assert res.evaluations == cfg.pop_size * (cfg.generations + 1)
    assert len(res.front_history) == cfg.generations + 1
    assert res.front_history[-1] == res.front


def test_front_is_mutually_non_dominated(trained_model) -> None:
    inst = _instance()
    res = run_attention_nsga2(inst, trained_model, AttentionNSGA2Config(20, generations=10, seed=1))
    front = res.front
    assert len(front) >= 1
    for i, (m_i, e_i) in enumerate(front):
        for j, (m_j, e_j) in enumerate(front):
            if i != j:
                assert not (m_j <= m_i and e_j <= e_i)
    assert len(res.schedules) == len(front)


def test_all_archive_schedules_are_feasible(trained_model) -> None:
    inst = _instance()
    res = run_attention_nsga2(inst, trained_model, AttentionNSGA2Config(20, generations=10, seed=2))
    for sched, obj in zip(res.schedules, res.front, strict=True):
        ev = evaluate(sched, inst)  # never raises ScheduleCycleError
        assert ev.objectives == pytest.approx(obj)


def test_pop_size_too_small_raises(trained_model) -> None:
    inst = _instance()
    with pytest.raises(ValueError, match="pop_size"):
        run_attention_nsga2(inst, trained_model, AttentionNSGA2Config(pop_size=1, generations=2))


@pytest.mark.slow
def test_front_bounded_by_oracle(trained_model) -> None:
    inst = _instance()
    res = run_attention_nsga2(inst, trained_model, default_config(inst, generations=60, seed=2))
    golden = _golden_front()
    tol = 1e-4
    for p in res.front:
        assert any(g[0] <= p[0] + tol and g[1] <= p[1] + tol for g in golden), p


@pytest.mark.slow
def test_swap_operator_is_exercised(trained_model) -> None:
    # The Kahn-guarded deadlock path must actually fire during a real run.
    inst = _instance()
    res = run_attention_nsga2(inst, trained_model, default_config(inst, generations=40, seed=0))
    assert res.deadlocks_rejected > 0
