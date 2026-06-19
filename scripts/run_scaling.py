"""Parallel scaling study for the physics-fused TAPE under peak-power coupling.

Each (N, peak_power, seed) configuration is an **independent** train+evaluate job, so we
fan them across a CPU process pool (one BLAS thread per worker to avoid oversubscription).
For every config we report the clean ablation:

- frozen-core **black-box MLP** head ``r2_makespan`` (the baseline that collapses), vs
- the **physics-fused tropical** head ``r2_makespan`` / ``r2_energy``, plus
- **leg-critical Jaccard** vs the exact coupled TAPE oracle (faithful attribution).

Run on the VM (uses all cores)::

    python scripts/run_scaling.py --tasks 6 8 10 12 --peak-power 30 --seeds 0 1 2 \\
        --workers 32 > experiments/scaling/run.log

Writes ``experiments/scaling/scaling_pp{budget}.json`` (one row per config + per-N means).
"""

from __future__ import annotations

import argparse
import json
import os
import statistics as st
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

OUT_DIR = Path(__file__).resolve().parents[1] / "experiments" / "scaling"


@dataclass(frozen=True)
class Job:
    num_tasks: int
    peak_power: float | None
    seed: int
    core_samples: int
    core_epochs: int
    fused_samples: int
    fused_epochs: int
    explain_samples: int


def _run_job(job: Job) -> dict[str, object]:
    """Train core + fused for one config and return the ablation metrics (worker process)."""
    import torch

    torch.set_num_threads(1)
    from ehgat.environment.decoder import NUM_BLOCKS, decode
    from ehgat.environment.evaluator import evaluate
    from ehgat.environment.instance import build_toy_instance
    from ehgat.explain.fused_explainer import faithfulness_report
    from ehgat.explain.train_fused import FusedTrainConfig, build_core, train_fused
    from ehgat.surrogate.graph import build_hetero_graph
    from ehgat.surrogate.train import regression_metrics
    from ehgat.utils.seeding import make_rng

    inst = build_toy_instance(num_tasks=job.num_tasks, peak_power=job.peak_power)
    core = build_core(
        inst, seed=job.seed, num_samples=job.core_samples, epochs=job.core_epochs
    )

    # Black-box scalar-head baseline R^2 on a fresh validation draw.
    core.eval()
    rng = make_rng(job.seed + 999)
    preds, trues = [], []
    with torch.no_grad():
        for _ in range(200):
            s = decode(rng.random(NUM_BLOCKS * inst.num_tasks), inst)
            ev = evaluate(s, inst)
            out, _ = core(build_hetero_graph(s, inst))
            preds.append((out * core.target_std + core.target_mean)[0].detach())
            trues.append(torch.tensor([ev.makespan, ev.energy]))
    core_m = regression_metrics(torch.stack(preds), torch.stack(trues))

    res = train_fused(
        inst, core,
        FusedTrainConfig(num_samples=job.fused_samples, epochs=job.fused_epochs, seed=job.seed),
    )

    rng2 = make_rng(job.seed + 7)
    scheds = [
        decode(rng2.random(NUM_BLOCKS * inst.num_tasks), inst)
        for _ in range(job.explain_samples)
    ]
    reps = [faithfulness_report(res.model, s, inst) for s in scheds]
    return {
        "num_tasks": job.num_tasks,
        "peak_power": job.peak_power,
        "seed": job.seed,
        "core_r2_makespan": round(core_m["r2_makespan"], 4),
        "fused_r2_makespan": round(res.metrics["r2_makespan"], 4),
        "fused_r2_energy": round(res.metrics["r2_energy"], 4),
        "leg_critical_jaccard": round(st.mean(r.leg_critical_jaccard for r in reps), 4),
        "cmax_abs_err": round(st.mean(r.makespan_abs_error for r in reps), 4),
    }


def _sizing(n: int) -> tuple[int, int, int, int]:
    """Scale sample/epoch budgets gently with N (core_samples, core_epochs, fused_samples, fused_epochs)."""
    core_samples = max(800, 150 * n)
    fused_samples = max(500, 90 * n)
    return core_samples, 50, fused_samples, 60


def main() -> None:
    ap = argparse.ArgumentParser(description="Parallel coupled scaling study (Req 2 / Tier-1).")
    ap.add_argument("--tasks", type=int, nargs="+", default=[6, 8, 10, 12])
    ap.add_argument("--peak-power", type=float, default=30.0)
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--explain-samples", type=int, default=24)
    ap.add_argument("--workers", type=int, default=min(os.cpu_count() or 4, 32))
    args = ap.parse_args()

    jobs: list[Job] = []
    for n in args.tasks:
        cs, ce, fs, fe = _sizing(n)
        for seed in args.seeds:
            jobs.append(Job(n, args.peak_power, seed, cs, ce, fs, fe, args.explain_samples))

    print(f"[scaling] {len(jobs)} jobs over {args.workers} workers "
          f"(tasks={args.tasks} seeds={args.seeds} peak_power={args.peak_power})", flush=True)

    rows: list[dict[str, object]] = []
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(_run_job, j): j for j in jobs}
        for fut in as_completed(futs):
            row = fut.result()
            rows.append(row)
            print(f"[scaling] N={row['num_tasks']} seed={row['seed']} "
                  f"core={row['core_r2_makespan']} fused={row['fused_r2_makespan']} "
                  f"jaccard={row['leg_critical_jaccard']}", flush=True)

    # Aggregate per-N means across seeds.
    per_n: dict[int, dict[str, float]] = {}
    for n in args.tasks:
        sub = [r for r in rows if r["num_tasks"] == n]
        per_n[n] = {
            "core_r2_makespan": round(st.mean(r["core_r2_makespan"] for r in sub), 4),
            "fused_r2_makespan": round(st.mean(r["fused_r2_makespan"] for r in sub), 4),
            "fused_r2_energy": round(st.mean(r["fused_r2_energy"] for r in sub), 4),
            "leg_critical_jaccard": round(st.mean(r["leg_critical_jaccard"] for r in sub), 4),
            "cmax_abs_err": round(st.mean(r["cmax_abs_err"] for r in sub), 4),
        }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tag = f"_pp{args.peak_power:g}" if args.peak_power is not None else "_uncoupled"
    out = OUT_DIR / f"scaling{tag}.json"
    out.write_text(json.dumps({"rows": rows, "per_n_mean": per_n}, indent=2))

    print("\n[scaling] per-N means (black-box core vs fused tropical):", flush=True)
    print(f"{'N':>4} {'core_r2':>9} {'fused_r2':>9} {'energy_r2':>10} {'jaccard':>8} {'cmax_err':>9}", flush=True)
    for n in args.tasks:
        m = per_n[n]
        print(f"{n:>4} {m['core_r2_makespan']:>9.3f} {m['fused_r2_makespan']:>9.3f} "
              f"{m['fused_r2_energy']:>10.3f} {m['leg_critical_jaccard']:>8.3f} "
              f"{m['cmax_abs_err']:>9.2f}", flush=True)
    print(f"[scaling] wrote {out}", flush=True)


if __name__ == "__main__":
    main()
