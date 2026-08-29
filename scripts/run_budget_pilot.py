"""Does surrogate faithfulness on the large instances recover with a scaled training budget?

The fused head is trained on a fixed number of self-supervised schedules regardless of instance
size. At the small instances that is 50--150 samples per leg, matching the configuration under
which the leg-critical Jaccard was previously reported at 0.95--1.00; at the largest dual-cycling
instance the same constant is under four samples per leg. This pilot varies the budget on two
instances and measures the Jaccard against it, to separate an under-trained model from a limit of
the architecture. If the curve rises towards the small-instance figure the cause is the budget;
if it plateaus well below, the cause is structural and no further compute will help.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def _one(job: tuple) -> dict:
    sys.path.insert(0, str(REPO / "src"))
    import numpy as np

    from ehgat.baselines.mp_brkga import MpBRKGAConfig, run_mp_brkga
    from ehgat.environment.decoder import decode
    from ehgat.environment.dsdl import load_dl_instances
    from ehgat.explain.fused_explainer import faithfulness_report
    from ehgat.explain.train_fused import FusedTrainConfig, build_core, train_fused

    name, per_leg, seed, gens = job
    inst = load_dl_instances(only=[name])[0].instance
    legs = 2 * inst.num_tasks
    n_samples = int(per_leg * legs)

    t0 = time.time()
    core = build_core(inst, num_samples=max(2000, n_samples), epochs=80, seed=seed)
    model = train_fused(inst, core, FusedTrainConfig(
        num_samples=n_samples, epochs=40, seed=seed))
    train_s = time.time() - t0

    res = run_mp_brkga(inst, MpBRKGAConfig(pop_size=20 * inst.num_tasks,
                                           generations=gens, seed=seed))
    scheds = [decode(np.asarray(c), inst) for c in res.chromosomes][:64]
    reps = [faithfulness_report(model, s, inst) for s in scheds]
    return {
        "instance": name, "num_tasks": inst.num_tasks, "legs": legs,
        "samples_per_leg": per_leg, "n_samples": n_samples, "seed": seed,
        "n_explained": len(reps),
        "leg_jaccard": float(np.mean([r.leg_critical_jaccard for r in reps])),
        "arc_jaccard": float(np.mean([r.arc_critical_jaccard for r in reps])),
        "makespan_abs_error": float(np.mean([r.makespan_abs_error for r in reps])),
        "train_s": train_s, "wall_s": time.time() - t0,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--instances", nargs="+", default=["DL03", "DL10"])
    ap.add_argument("--per-leg", nargs="+", type=float, default=[4, 12, 25, 50])
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--generations", type=int, default=60)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--out", type=Path, default=REPO / "experiments" / "thesis" / "budget_pilot.json")
    args = ap.parse_args()

    from concurrent.futures import ProcessPoolExecutor, as_completed
    jobs = [(n, pl, s, args.generations)
            for n in args.instances for pl in args.per_leg for s in range(args.seeds)]
    print(f"[pilot] {len(jobs)} fits over {args.workers} workers", flush=True)
    rows, t0 = [], time.time()
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(_one, j): j for j in jobs}
        for i, f in enumerate(as_completed(futs), 1):
            try:
                r = f.result(); rows.append(r)
                print(f"  {r['instance']} per_leg={r['samples_per_leg']:g} "
                      f"seed={r['seed']}: legJ={r['leg_jaccard']:.3f} "
                      f"({r['train_s']:.0f}s train)", flush=True)
            except Exception as exc:
                print(f"  FAILED {futs[f][:3]}: {type(exc).__name__}: {exc}", flush=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"rows": rows}, indent=2))
    print(f"[pilot] wrote {args.out} in {(time.time()-t0)/60:.1f} min")


if __name__ == "__main__":
    main()
