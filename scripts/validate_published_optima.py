"""Check the reconstructed instances against the optima the source publishes for them.

Every instance family in this project is reconstructed from printed tables, so each carries the
risk that the reconstruction is wrong in a way no internal check would catch. The published MILP
optima are the external check: a front computed on a correctly reconstructed instance cannot beat
a proven optimum, so its makespan-optimal end must lie at or above the published C*max and its
energy-optimal end at or above the published E*. A value below one of those means the instance is
easier than the published one, which is a fault in the reconstruction rather than a success of
the solver. Runs are at the published fleet size so that the comparison is like for like.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PARSED = REPO / "data" / "Container_Transport_Parsed_Tables" / "container_transport_tables_1_to_5.json"


def _worker(job: tuple) -> dict:
    sys.path.insert(0, str(REPO / "src"))
    from dataclasses import replace as _replace

    import numpy as np
    from ehgat.baselines.mp_brkga import MpBRKGAConfig, run_mp_brkga
    from ehgat.environment.dsdl import load_dsdl_instance, load_tables_4_5

    name, rec, num_agvs, seed, gens = job
    ref = load_tables_4_5(str(REPO / "data" / "tables_4_5.json"), only=["L01"])[0]
    base = load_dsdl_instance(name, rec, distance=ref.instance.distance).instance
    inst = _replace(base, num_agvs=num_agvs)
    res = run_mp_brkga(inst, MpBRKGAConfig(pop_size=20 * inst.num_tasks,
                                           generations=gens, seed=seed))
    front = sorted(res.front)
    return {"instance": name, "seed": seed, "num_agvs": num_agvs,
            "cmax_min": front[0][0], "energy_at_cmax_min": front[0][1],
            "energy_min": min(e for _, e in front),
            "cmax_at_energy_min": max(front)[0], "n_front": len(front)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--family", choices=("mixed", "unloading"), required=True)
    ap.add_argument("--agvs", type=int, default=2)
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--generations", type=int, default=300)
    ap.add_argument("--workers", type=int, default=120)
    args = ap.parse_args()

    fam = json.loads((REPO / "data" / "instance_families.json").read_text())
    parsed = json.loads(PARSED.read_text())["tables"]

    if args.family == "mixed":
        pub = {r["instance"]: r["dual_cycling"] for r in parsed["table_3"]["rows"]}
        names = [k for k, v in fam.items() if isinstance(v, dict) and v.get("family") == "mixed"]
    else:
        # Table 2 nests its values per speed scenario. The nominal-higher scenario is the
        # nearest comparison to the three-speed selection used here, as it permits the highest
        # fixed speed; its C*max is the makespan optimum and Scen.N's E* the energy optimum.
        pub = {}
        for r in parsed["table_2"]["rows"]:
            nh = r.get("scenario_n_tilde_h") or {}
            sn = r.get("scenario_n") or {}
            # Table 2 splits one front across two scenario columns exactly as Table 3 does:
            # Scen.L~N carries the energy-optimal end and Scen.N~H the makespan-optimal end.
            # Taking E* from Scen.N instead compares against a different (nominal fixed-speed)
            # front and makes the check meaningless.
            ln = r.get("scenario_l_tilde_n") or {}
            pub[f"U_L{r['instance'][1:]}"] = {
                "c_max_star": nh.get("c_max_star"),
                "energy_star": ln.get("energy_star") or sn.get("energy_star"),
            }
        names = [k for k, v in fam.items() if isinstance(v, dict) and v.get("family") == "unloading"]

    jobs = [(n, fam[n], args.agvs, s, args.generations) for n in sorted(names)
            for s in range(args.seeds)]
    print(f"[validate:{args.family}] {len(jobs)} runs at A={args.agvs}, "
          f"Gmax={args.generations}, over {args.workers} workers", flush=True)

    best: dict[str, dict] = {}
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(_worker, j) for j in jobs]
        for i, f in enumerate(as_completed(futs), 1):
            r = f.result()
            b = best.setdefault(r["instance"], r)
            if r["cmax_min"] < b["cmax_min"]:
                b["cmax_min"] = r["cmax_min"]
            if r["energy_min"] < b["energy_min"]:
                b["energy_min"] = r["energy_min"]
            if i % 50 == 0:
                print(f"  {i}/{len(jobs)}", flush=True)

    out = {"family": args.family, "agvs": args.agvs, "generations": args.generations,
           "seeds": args.seeds, "rows": []}
    print(f"\n  {'ins':<8}{'our Cmax':>10}{'pub C*max':>11}{'ok':>4}"
          f"{'our E':>10}{'pub E*':>10}{'ok':>4}")
    viol = 0
    for n in sorted(best):
        b = best[n]
        p = pub.get(n if args.family == "mixed" else n, {})
        pc = p.get("c_max_star"); pe = p.get("energy_star")
        okc = pc is None or b["cmax_min"] >= pc - 1e-6
        oke = pe is None or b["energy_min"] >= pe - 1e-6
        viol += (not okc) + (not oke)
        out["rows"].append({**b, "pub_cmax_star": pc, "pub_energy_star": pe,
                            "cmax_ok": okc, "energy_ok": oke})
        print(f"  {n:<8}{b['cmax_min']:>10.1f}{str(pc):>11}{'y' if okc else 'NO':>4}"
              f"{b['energy_min']:>10.0f}{str(pe):>10}{'y' if oke else 'NO':>4}")
    out["violations"] = viol
    dest = REPO / "experiments" / "thesis" / f"validate_{args.family}.json"
    dest.write_text(json.dumps(out, indent=2))
    print(f"\n[validate:{args.family}] {viol} violation(s) of the published optima -> {dest}")


if __name__ == "__main__":
    main()
