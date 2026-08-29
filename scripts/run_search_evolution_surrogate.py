"""The surrogate as a way to compare how explanations change during the search.

This is the second of the two roles the supervisor assigns the surrogate. The first, explaining
finalised solutions, is reported in Chapter 4. This one asks whether the model can also track the
explanation while the search is still running, which is the precondition for ever using it to
steer that search.

One model is fitted per instance and fleet size and reused across seeds, since the model depends
on the instance and not on the random stream. At every archive snapshot both attributions are
computed: the exact one from the tropical oracle, and the model's own, whose gradients are
weighted by the model's own predicted durations so that the two explanations are never mixed.
The reported quantity is therefore not only how the explanation moves, but whether the learned
model moves with it.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

FAMILY_INSTANCES = {
    "loading":   ("L_L01", "L_L07", "L_L15", "L_L21", "L_L28", "L_L35"),
    "unloading": ("U_L01", "U_L07", "U_L15", "U_L21", "U_L28", "U_L35"),
    # six of the published dual-cycling instances, spanning the three crane counts and all
    # three task sizes: D01/D06 at 8 tasks, D10/D13 at 12, D19/D21 at 16
    "mixed":     ("D01", "D06", "D10", "D13", "D19", "D21"),
}


def _cell(job: tuple) -> dict:
    """One (instance, fleet) cell: fit once, then every seed's whole search trajectory."""
    sys.path.insert(0, str(REPO / "src"))
    import numpy as np
    import torch
    torch.set_num_threads(1)
    from dataclasses import replace as _replace

    from ehgat.baselines.mp_brkga import MpBRKGAConfig, run_mp_brkga
    from ehgat.environment.decoder import decode
    from ehgat.environment.dsdl import load_dsdl_instance, load_tables_4_5
    from ehgat.explain.critical_share import critical_path_shares, exact_critical_shares
    from ehgat.explain.fused_explainer import explain_fused
    from ehgat.explain.train_fused import FusedTrainConfig, build_core, train_fused
    from ehgat.surrogate.graph import build_hetero_graph

    name, num_agvs, seeds, gens, every, per_leg = job
    doc = json.loads((REPO / "data" / "instance_families.json").read_text())
    ref = load_tables_4_5(str(REPO / "data" / "tables_4_5.json"), only=["L01"])[0]
    base = load_dsdl_instance(name, doc[name], distance=ref.instance.distance).instance
    inst = _replace(base, num_agvs=num_agvs)
    legs = 2 * inst.num_tasks

    t0 = time.time()
    core = build_core(inst, num_samples=2000, epochs=80, seed=0)
    fitted = train_fused(inst, core, FusedTrainConfig(
        num_samples=max(1200, int(per_leg * legs)), epochs=40, seed=0))
    model = fitted.model.cpu()          # train_fused returns a result object, not the model
    calib = {k: float(v) for k, v in fitted.metrics.items()}
    train_s = time.time() - t0

    def model_share(sched):
        with torch.no_grad():
            pr = model(build_hetero_graph(sched, inst))
            et = tuple(float(v) for v in pr.empty_t.detach().cpu())
            lt = tuple(float(v) for v in pr.loaded_t.detach().cpu())
            nd = tuple(float(v) for v in pr.node_delay.detach().cpu())
        return critical_path_shares(explain_fused(model, sched, inst), et, lt, nd)

    out_seeds = []
    for seed in range(seeds):
        res = run_mp_brkga(inst, MpBRKGAConfig(pop_size=20 * inst.num_tasks, generations=gens,
                                               seed=seed, snapshot_every=every))
        snaps = []
        for gen, objs, chroms in res.chrom_snapshots:
            ex_pts, md_pts = [], []
            for chi, (cmax, energy) in zip(chroms, objs):
                sched = decode(np.asarray(chi), inst)
                ex = exact_critical_shares(sched, inst)
                if not ex.closes or math.isnan(ex.transport):
                    continue
                md = model_share(sched)
                ex_pts.append((float(cmax), ex.transport))
                md_pts.append(md.transport if md.closes and not math.isnan(md.transport) else None)
            if not ex_pts:
                continue
            order = sorted(range(len(ex_pts)), key=lambda i: ex_pts[i][0])
            ex_sorted = [ex_pts[i][1] for i in order]
            md_sorted = [md_pts[i] for i in order]
            rec = {"gen": gen, "n": len(ex_sorted),
                   "exact_migration": ex_sorted[0] - ex_sorted[-1]}
            if md_sorted[0] is not None and md_sorted[-1] is not None:
                rec["model_migration"] = md_sorted[0] - md_sorted[-1]
                rec["abs_error"] = abs(rec["model_migration"] - rec["exact_migration"])
            paired = [(e, m) for e, m in zip(ex_sorted, md_sorted) if m is not None]
            if paired:
                rec["mean_abs_share_error"] = float(
                    np.mean([abs(m - e) for e, m in paired]))
                rec["n_model_closed"] = len(paired)
            snaps.append(rec)
        out_seeds.append({"seed": seed, "snapshots": snaps})

    return {"instance": name, "num_agvs": num_agvs, "num_qcs": len(inst.qcs),
            "agv_per_qc": num_agvs / len(inst.qcs), "num_tasks": inst.num_tasks,
            "samples_per_leg": per_leg, "train_s": train_s, "calibration": calib,
            "wall_s": time.time() - t0, "seeds": out_seeds}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fleet", default="2,4,6")
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--generations", type=int, default=100)
    ap.add_argument("--every", type=int, default=10)
    ap.add_argument("--per-leg", type=float, default=50.0)
    ap.add_argument("--workers", type=int, default=54)
    ap.add_argument("--out", type=Path,
                    default=REPO / "experiments" / "thesis" / "search_evolution_surrogate.json")
    args = ap.parse_args()

    fleet = [int(x) for x in args.fleet.split(",")]
    names = [n for fam in FAMILY_INSTANCES.values() for n in fam]
    jobs = [(n, a, args.seeds, args.generations, args.every, args.per_leg)
            for n in names for a in fleet]
    print(f"[evo-surrogate] {len(jobs)} cells (one fit each) x {args.seeds} seeds "
          f"over {args.workers} workers", flush=True)

    rows, t0 = [], time.time()
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(_cell, j): j for j in jobs}
        for i, f in enumerate(as_completed(futs), 1):
            try:
                r = f.result(); rows.append(r)
                errs = [sn.get("abs_error") for s in r["seeds"] for sn in s["snapshots"]
                        if sn.get("abs_error") is not None]
                m = sum(errs) / len(errs) if errs else float("nan")
                print(f"  [{i}/{len(jobs)}] {r['instance']} A={r['num_agvs']} "
                      f"mean|model-exact| migration err {m:.3f} ({r['train_s']:.0f}s fit)",
                      flush=True)
            except Exception as exc:
                print(f"  FAILED {futs[f][:2]}: {type(exc).__name__}: {exc}", flush=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(
        {"config": {"fleet": fleet, "seeds": args.seeds, "generations": args.generations,
                    "snapshot_every": args.every, "samples_per_leg": args.per_leg,
                    "instances": names}, "per_cell": rows}, indent=2))
    print(f"[evo-surrogate] wrote {args.out} in {(time.time()-t0)/60:.1f} min")


if __name__ == "__main__":
    main()
