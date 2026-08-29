"""How the explanation changes during the search, not only at its end.

Every result elsewhere in this project explains *finalised* solutions: the front campaign
resolves the transport share at every point of every front, but each of those fronts is the
output of a completed run. This campaign asks the prior question of whether the explanation of
a front is already settled early in the search or continues to move as the front converges.

The design follows Fig. 5 of the source work, which reports the impact of the generation budget
by overlaying the front obtained at several values of ``Gmax`` on the objective plane. The same
overlay is produced here, with the addition that every point carries its duration-weighted
transport share, so the figure reports how the front and its explanation converge together.
Snapshots come from the solver's own archive rather than from re-running at each budget, which
is exact and costs nothing beyond the memory of retaining the chromosomes.
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

# the six instances of the migration sweep, so the two results are directly comparable
INSTANCES = ("L01", "L07", "L15", "L21", "L28", "L35")

# Equivalents drawn from each of the three families of Section 4.6, so that the during-search
# result is established on the same breadth as the threshold result rather than on loading alone.
FAMILY_INSTANCES = {
    "loading":   ("L_L01", "L_L07", "L_L15", "L_L21", "L_L28", "L_L35"),
    "unloading": ("U_L01", "U_L07", "U_L15", "U_L21", "U_L28", "U_L35"),
    "mixed":     ("D_L01_L18", "D_L05_L06", "D_L07_L08", "D_L11_L12", "D_L15_L16", "D_L21_L22"),
}


def _worker(job: tuple) -> dict:
    sys.path.insert(0, str(REPO / "src"))
    sys.path.insert(0, str(REPO / "scripts"))
    import numpy as np
    from run_thesis_experiments import _load

    from ehgat.baselines.mp_brkga import MpBRKGAConfig, run_mp_brkga
    from ehgat.environment.decoder import decode
    from ehgat.explain.critical_share import exact_critical_shares

    name, num_agvs, seed, gens, every = job
    if name in ("L01", "L07", "L15", "L21", "L28", "L35"):
        inst = _load(name, num_agvs)
    else:
        from dataclasses import replace as _replace

        from ehgat.environment.dsdl import load_dsdl_instance, load_tables_4_5
        doc = json.loads((REPO / "data" / "instance_families.json").read_text())
        ref = load_tables_4_5(str(REPO / "data" / "tables_4_5.json"), only=["L01"])[0]
        base = load_dsdl_instance(name, doc[name], distance=ref.instance.distance).instance
        inst = _replace(base, num_agvs=num_agvs)
    t0 = time.time()
    res = run_mp_brkga(inst, MpBRKGAConfig(pop_size=20 * inst.num_tasks, generations=gens,
                                           seed=seed, snapshot_every=every))
    snaps = []
    for gen, objs, chroms in res.chrom_snapshots:
        pts, n_open = [], 0
        for chi, (cmax, energy) in zip(chroms, objs):
            sh = exact_critical_shares(decode(np.asarray(chi), inst), inst)
            if not sh.closes or math.isnan(sh.transport):
                n_open += 1
                continue
            pts.append({"cmax": float(cmax), "energy": float(energy),
                        "rho": float(sh.transport)})
        pts.sort(key=lambda q: q["cmax"])
        rec = {"gen": gen, "n": len(pts), "n_open": n_open, "front": pts}
        if pts:
            rec["rho_makespan_end"] = pts[0]["rho"]
            rec["rho_energy_end"] = pts[-1]["rho"]
            rec["migration"] = pts[0]["rho"] - pts[-1]["rho"]
        snaps.append(rec)
    return {"instance": name, "num_agvs": num_agvs, "num_qcs": len(inst.qcs),
            "agv_per_qc": num_agvs / len(inst.qcs), "seed": seed,
            "wall_s": time.time() - t0, "snapshots": snaps}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fleet", default="2,4,6", help="fleet sizes, spanning the threshold")
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--generations", type=int, default=100)
    ap.add_argument("--every", type=int, default=10)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--families", action="store_true",
                    help="run six instances from each of the three families instead of the "
                         "six swept loading instances")
    ap.add_argument("--out", type=Path,
                    default=REPO / "experiments" / "thesis" / "search_evolution.json")
    args = ap.parse_args()

    fleet = [int(x) for x in args.fleet.split(",")]
    names = ([n for fam in FAMILY_INSTANCES.values() for n in fam]
             if args.families else list(INSTANCES))
    jobs = [(n, a, s, args.generations, args.every)
            for n in names for a in fleet for s in range(args.seeds)]
    print(f"[evolution] {len(jobs)} replicates over {args.workers} workers", flush=True)

    rows, failed, t0 = [], 0, time.time()
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(_worker, j): j for j in jobs}
        for i, f in enumerate(as_completed(futs), 1):
            try:
                rows.append(f.result())
            except Exception as exc:
                failed += 1
                print(f"  FAILED {futs[f][:3]}: {type(exc).__name__}: {exc}", flush=True)
            if i % 20 == 0 or i == len(jobs):
                el = time.time() - t0
                print(f"  {i}/{len(jobs)}  {el/60:.1f} min elapsed", flush=True)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(
        {"config": {"instances": names, "families": bool(args.families),
                    "fleet": fleet, "seeds": args.seeds,
                    "generations": args.generations, "snapshot_every": args.every},
         "per_seed": rows}, indent=2))
    print(f"[evolution] wrote {args.out}  ({len(rows)} rows, {failed} failed)")


if __name__ == "__main__":
    main()
