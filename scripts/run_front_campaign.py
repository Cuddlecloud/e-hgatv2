"""Front-behaviour campaign over the three small-instance families.

For every (instance, fleet size, seed) this solves the bi-objective problem with mp-BRKGA and
then computes the duration-weighted critical share at *every* point of the resulting front, not
only at the two extremes. The extremes give the migration reported previously; the full profile
gives how the binding resource changes across the front, which the two-point measurement cannot
show.

No surrogate is fitted. Every quantity here comes from the exact evaluator and the exact
tropical attribution, so a replicate costs a few seconds and needs no GPU.

Writes one JSON per shard so that a partial run is still usable, plus a merged file.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import replace
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def _worker(job: tuple) -> dict:
    import sys
    sys.path.insert(0, str(REPO / "src"))
    import numpy as np
    from ehgat.baselines.mp_brkga import run_mp_brkga, MpBRKGAConfig
    from ehgat.environment.dsdl import load_dsdl_instance, load_tables_4_5
    from ehgat.environment.decoder import decode
    from ehgat.explain.critical_share import exact_critical_shares

    name, rec, num_agvs, seed, generations = job
    ref = load_tables_4_5(str(REPO / "data" / "tables_4_5.json"), only=["L01"])[0]
    base = load_dsdl_instance(name, rec, distance=ref.instance.distance).instance
    inst = replace(base, num_agvs=num_agvs)

    t0 = time.time()
    res = run_mp_brkga(inst, MpBRKGAConfig(pop_size=20 * inst.num_tasks,
                                           generations=generations, seed=seed))
    solve_s = time.time() - t0

    pts, n_open = [], 0
    for chi, (cmax, energy) in zip(res.chromosomes, res.front):
        sh = exact_critical_shares(decode(np.asarray(chi), inst), inst)
        if not sh.closes or math.isnan(sh.transport):
            n_open += 1
            continue
        pts.append({"cmax": float(cmax), "energy": float(energy),
                    "rho": float(sh.transport)})
    pts.sort(key=lambda p: p["cmax"])

    out = {"instance": name, "family": rec["family"], "source": rec["source"],
           "num_tasks": inst.num_tasks, "num_qcs": len(inst.qcs), "num_agvs": num_agvs,
           "agv_per_qc": num_agvs / len(inst.qcs), "seed": seed,
           "n_front": len(res.front), "n_closed": len(pts), "n_open": n_open,
           "evaluations": int(res.evaluations), "solve_s": solve_s,
           "wall_s": time.time() - t0, "front": pts}
    if pts:
        mk, en = pts[0], pts[-1]          # sorted by makespan: first is makespan-optimal
        out["rho_makespan_end"] = mk["rho"]
        out["rho_energy_end"] = en["rho"]
        out["migration"] = mk["rho"] - en["rho"]     # matches critical_share.migration
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--families", default="loading,unloading,mixed")
    ap.add_argument("--fleet", default="1,2,3,4,5,6,7,8,9")
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--generations", type=int, default=100)
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--limit", type=int, default=0, help="smoke test: cap the job count")
    ap.add_argument("--out", type=Path, default=REPO / "experiments" / "front_campaign")
    args = ap.parse_args()

    doc = json.loads((REPO / "data" / "instance_families.json").read_text())
    fams = set(args.families.split(","))
    fleet = [int(x) for x in args.fleet.split(",")]

    jobs = [(name, rec, a, s, args.generations)
            for name, rec in doc.items() if name != "_provenance" and rec["family"] in fams
            for a in fleet for s in range(args.seeds)]
    if args.limit:
        jobs = jobs[:args.limit]

    args.out.mkdir(parents=True, exist_ok=True)
    print(f"[campaign] {len(jobs)} replicates over {args.workers} workers", flush=True)
    t0, done, rows, failed = time.time(), 0, [], 0
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(_worker, j): j for j in jobs}
        for f in as_completed(futs):
            done += 1
            try:
                rows.append(f.result())
            except Exception as exc:
                failed += 1
                print(f"  FAILED {futs[f][0]} A={futs[f][2]} s={futs[f][3]}: "
                      f"{type(exc).__name__}: {exc}", flush=True)
            if done % 200 == 0 or done == len(jobs):
                el = time.time() - t0
                print(f"  {done}/{len(jobs)}  {el/60:.1f} min elapsed, "
                      f"{el/done*(len(jobs)-done)/60:.1f} min remaining", flush=True)

    merged = args.out / "front_campaign.json"
    merged.write_text(json.dumps(
        {"config": {"families": sorted(fams), "fleet": fleet, "seeds": args.seeds,
                    "generations": args.generations, "n_jobs": len(jobs),
                    "failed": failed},
         "per_seed": rows}, indent=1))
    print(f"[campaign] wrote {merged}  ({len(rows)} rows, {failed} failed, "
          f"{(time.time()-t0)/60:.1f} min)")


if __name__ == "__main__":
    main()
