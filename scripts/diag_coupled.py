"""Diagnose the coupled R^2 ceiling: frozen-core scalar head vs the fused wait-head.

Locates whether the makespan-R^2 limit under peak-power coupling is the frozen embedding
core (its own scalar regression head) or the fused tropical head / wait predictions.

Run (on the VM, thread-limited so the per-graph Python loops don't oversubscribe)::

    OMP_NUM_THREADS=4 python scripts/diag_coupled.py --tasks 8 --peak-power 30 \\
        --core-samples 1500 --core-epochs 60 --fused-samples 800 --fused-epochs 60
"""

from __future__ import annotations

import argparse
import statistics as st
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ehgat.environment.decoder import NUM_BLOCKS, decode
from ehgat.environment.evaluator import evaluate
from ehgat.environment.instance import build_toy_instance
from ehgat.explain.fused_explainer import faithfulness_report
from ehgat.explain.train_fused import FusedTrainConfig, build_core, train_fused
from ehgat.surrogate.graph import build_hetero_graph
from ehgat.surrogate.train import regression_metrics
from ehgat.utils.seeding import make_rng


def _core_r2(core, inst, n_val: int = 300) -> dict[str, float]:
    core.eval()
    rng = make_rng(123)
    preds, trues = [], []
    with torch.no_grad():
        for _ in range(n_val):
            s = decode(rng.random(NUM_BLOCKS * inst.num_tasks), inst)
            ev = evaluate(s, inst)
            out, _ = core(build_hetero_graph(s, inst))
            pred = out * core.target_std + core.target_mean
            preds.append(pred[0].detach())
            trues.append(torch.tensor([ev.makespan, ev.energy]))
    return regression_metrics(torch.stack(preds), torch.stack(trues))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", type=int, default=8)
    ap.add_argument("--peak-power", type=float, default=30.0)
    ap.add_argument("--core-samples", type=int, default=1500)
    ap.add_argument("--core-epochs", type=int, default=60)
    ap.add_argument("--fused-samples", type=int, default=800)
    ap.add_argument("--fused-epochs", type=int, default=60)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    torch.set_num_threads(args.threads)
    inst = build_toy_instance(num_tasks=args.tasks, peak_power=args.peak_power)
    print(f"[diag] N={args.tasks} peak_power={args.peak_power} threads={args.threads}", flush=True)

    core = build_core(
        inst, seed=args.seed, num_samples=args.core_samples, epochs=args.core_epochs
    )
    cm = _core_r2(core, inst)
    print(f"[diag] CORE scalar-head r2_makespan={cm['r2_makespan']:.4f} "
          f"r2_energy={cm['r2_energy']:.4f}", flush=True)

    res = train_fused(
        inst, core,
        FusedTrainConfig(num_samples=args.fused_samples, epochs=args.fused_epochs, seed=args.seed),
    )
    fm = res.metrics
    print(f"[diag] FUSED wait-head r2_makespan={fm['r2_makespan']:.4f} "
          f"r2_energy={fm['r2_energy']:.4f}", flush=True)

    rng = make_rng(7)
    scheds = [decode(rng.random(NUM_BLOCKS * inst.num_tasks), inst) for _ in range(24)]
    reps = [faithfulness_report(res.model, s, inst) for s in scheds]
    print(f"[diag] faithfulness leg_jaccard="
          f"{st.mean(r.leg_critical_jaccard for r in reps):.4f} "
          f"cmax_abs_err={st.mean(r.makespan_abs_error for r in reps):.4f}", flush=True)
    print("[diag] DONE", flush=True)


if __name__ == "__main__":
    main()
