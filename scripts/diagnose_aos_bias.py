"""scripts/diagnose_aos_bias.py -- diagnose why the Channel-B AOS arms are indistinguishable.

Hypothesis: the controller aggregates the per-task AGV-vs-QC bottleneck into a single
population-averaged scalar ``bias`` per generation. Averaging many per-task values
regresses ``bias -> 0.5``, where ``operator_probabilities`` is ~uniform, so the
attention/oracle arms collapse onto random. This script measures the actual ``bias``
distribution (per-schedule and front-averaged) for both signal sources, plus the
resulting operator distributions, to confirm or refute that.

Usage (on the pod):
    python scripts/diagnose_aos_bias.py --tasks 10 --samples 64
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np

from ehgat.benchmark.faithfulness import critical_path_binding
from ehgat.environment.decoder import NUM_BLOCKS, decode
from ehgat.environment.instance import build_toy_instance
from ehgat.search.attention_nsga2 import (
    _MUTATION_OPS,
    attention_bottleneck_type,
    attention_task_probabilities,
    operator_probabilities,
)
from ehgat.surrogate.train import TrainConfig, train_surrogate
from ehgat.utils.seeding import make_rng


def _summary(name: str, values: np.ndarray) -> None:
    q = np.quantile(values, [0.0, 0.25, 0.5, 0.75, 1.0])
    print(
        f"  {name:18s} mean={values.mean():.3f} std={values.std():.3f} "
        f"min/med/max=[{q[0]:.3f}, {q[2]:.3f}, {q[4]:.3f}]"
    )


def _print_ops(label: str, probs: np.ndarray) -> None:
    pairs = ", ".join(f"{op}={p:.2f}" for op, p in zip(_MUTATION_OPS, probs, strict=True))
    print(f"  {label:24s} {pairs}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Diagnose AOS Channel-B bias washout")
    parser.add_argument("--tasks", type=int, default=10)
    parser.add_argument("--samples", type=int, default=64)
    parser.add_argument("--surrogate-samples", type=int, default=600)
    parser.add_argument("--surrogate-epochs", type=int, default=20)
    parser.add_argument("--operator-temp", type=float, default=0.5)
    parser.add_argument("--mutation-temp", type=float, default=0.25)
    ns = parser.parse_args()

    instance = build_toy_instance(num_tasks=ns.tasks)
    rng = make_rng(0)
    n = instance.num_tasks
    schedules = [decode(rng.random(NUM_BLOCKS * n), instance) for _ in range(ns.samples)]

    print(f"Training surrogate ({ns.surrogate_samples}/{ns.surrogate_epochs})...", flush=True)
    model = train_surrogate(
        instance, TrainConfig(num_samples=ns.surrogate_samples, epochs=ns.surrogate_epochs)
    ).model
    model.eval()

    # Per-schedule oracle bias (model-free, exact).
    oracle_bias = []
    for s in schedules:
        agv, qc = critical_path_binding(s, instance)
        total = len(agv) + len(qc)
        oracle_bias.append(len(agv) / total if total else 0.5)
    oracle_bias = np.asarray(oracle_bias)

    # Per-schedule attention bias (the learned readout used by the controller).
    attn_bias = []
    for s in schedules:
        w_agv, _ = attention_bottleneck_type(s, instance, model)
        p = attention_task_probabilities(s, instance, model, temperature=ns.mutation_temp)
        attn_bias.append(float(np.dot(p, w_agv)))
    attn_bias = np.asarray(attn_bias)

    print("\n=== Per-schedule bias distributions (1.0=AGV-bound, 0.0=QC-bound) ===")
    _summary("oracle bias", oracle_bias)
    _summary("attention bias", attn_bias)

    # Front-averaged bias = what the controller actually feeds operator_probabilities.
    print("\n=== Front-averaged bias (controller input; closer to 0.5 = weaker) ===")
    print(f"  oracle    front-mean = {oracle_bias.mean():.3f}")
    print(f"  attention front-mean = {attn_bias.mean():.3f}")

    print(f"\n=== Operator distributions at observed bias (temp={ns.operator_temp}) ===")
    _print_ops("random (uniform)", np.full(len(_MUTATION_OPS), 1.0 / len(_MUTATION_OPS)))
    _print_ops("oracle @ front-mean", operator_probabilities(oracle_bias.mean(), ns.operator_temp))
    _print_ops("attention @ front-mean", operator_probabilities(attn_bias.mean(), ns.operator_temp))
    print("  --- achievable spread at extremes ---")
    _print_ops("bias=0.0 (pure QC)", operator_probabilities(0.0, ns.operator_temp))
    _print_ops("bias=1.0 (pure AGV)", operator_probabilities(1.0, ns.operator_temp))

    # Verdict.
    spread = max(abs(oracle_bias.mean() - 0.5), abs(attn_bias.mean() - 0.5))
    print(
        f"\nVERDICT: max |front-mean - 0.5| = {spread:.3f}. "
        + ("BIAS WASHOUT CONFIRMED (controller ~uniform => arms collapse to random)."
           if spread < 0.1 else "bias is non-trivial; washout is NOT the main cause.")
    )


if __name__ == "__main__":
    main()
