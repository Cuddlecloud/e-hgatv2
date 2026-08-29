"""Head-to-head fidelity comparison: our mp-BRKGA against the author's own DL scripts.

The author's scripts are self-contained (geometry, task data and parameters are all inlined) and
are converted to headless form by ``scripts/make_headless_mp_brkga.py``. This script runs *our*
implementation on the same instance at the same published budget and reports the two front
extremes side by side.

The extremes are the right basis for comparison. They are convention-free -- ``min Cmax`` and
``min E`` over the final front -- whereas front cardinality and spread depend on archive
bookkeeping and, in his case, on a non-standard ``Delta`` that fixes ``db = du = 0``. Agreement
on the extremes is the claim the thesis actually rests on; agreement on cardinality is not.

Usage::

    python scripts/compare_mp_brkga_fidelity.py --instance DL01 --seeds 2 \
        --his /tmp/his_DL01_full.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

DL_MATRIX = ROOT / "data" / "dl_distance_matrix.csv"
DL_DATA = ROOT / "data" / "dl_instances.json"


def run_ours(instance_id: str, seeds: int, generations: int, verbose: bool) -> dict:
    from ehgat.baselines.mp_brkga import MpBRKGAConfig, run_mp_brkga
    from ehgat.environment.dsdl import load_dl_instances

    record = load_dl_instances(DL_DATA, matrix_path=DL_MATRIX, only=[instance_id])[0]
    instance = record.instance
    n = instance.num_tasks

    front: list[tuple[float, float]] = []
    times: list[float] = []
    for seed in range(seeds):
        cfg = MpBRKGAConfig(pop_size=20 * n, generations=generations, seed=seed)
        t0 = time.time()
        result = run_mp_brkga(instance, cfg)
        times.append(time.time() - t0)
        front.extend((float(a), float(b)) for a, b in result.front)
        if verbose:
            mk = min(front, key=lambda p: (p[0], p[1]))
            en = min(front, key=lambda p: (p[1], p[0]))
            print(
                f"  seed {seed}: |PF|={len(result.front)} "
                f"min_Cmax={mk[0]:.3f} min_E={en[1]:.3f} ({times[-1]:.1f}s)",
                flush=True,
            )

    # Pool the replications exactly as he does: his ``best`` array takes the min over REP.
    front.sort()
    mk = min(front, key=lambda p: (p[0], p[1]))
    en = min(front, key=lambda p: (p[1], p[0]))
    return {
        "source": "ours",
        "instance": instance_id,
        "rep": seeds,
        "gmax": generations,
        "pop_max": 20 * n,
        "n_tasks": n,
        "num_agvs": instance.num_agvs,
        "num_qcs": len(instance.qcs),
        "front": front,
        "front_size": len(front),
        "makespan_min": mk[0],
        "energy_at_makespan_min": mk[1],
        "energy_min": en[1],
        "makespan_at_energy_min": en[0],
        "time_mean": sum(times) / len(times),
        "synthetic_geometry": bool(getattr(record, "synthetic_geometry", False)),
    }


def report(ours: dict, his: dict | None) -> None:
    print("\n" + "=" * 74)
    print(f"mp-BRKGA fidelity -- {ours['instance']}")
    print("=" * 74)
    if his is None:
        print("(author's run not supplied; showing ours only)")
    for key in ("n_tasks", "num_qcs", "num_agvs", "pop_max", "gmax", "rep"):
        h = his.get(key, "-") if his else "-"
        flag = "" if his is None or h == ours.get(key) else "   <-- DIFFERS"
        print(f"  {key:24s} ours={ours.get(key)!s:>12s}   his={h!s:>12s}{flag}")
    print("-" * 74)
    rows = [
        ("min Cmax", "makespan_min"),
        ("  E at min Cmax", "energy_at_makespan_min"),
        ("min E", "energy_min"),
        ("  Cmax at min E", "makespan_at_energy_min"),
        ("|PF|", "front_size"),
    ]
    for label, key in rows:
        o = ours.get(key)
        if his is None:
            print(f"  {label:24s} ours={o:>14.3f}")
            continue
        h = his.get(key)
        if isinstance(o, float) and isinstance(h, (int, float)) and h:
            rel = (o - h) / abs(h) * 100.0
            print(f"  {label:24s} ours={o:>14.3f}   his={h:>14.3f}   {rel:+7.3f}%")
        else:
            print(f"  {label:24s} ours={o:>14}   his={h:>14}")
    print("=" * 74)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance", default="DL01")
    ap.add_argument("--seeds", type=int, default=2, help="matches his REP")
    ap.add_argument("--generations", type=int, default=300, help="matches his Gmax")
    ap.add_argument("--his", default=None, help="JSON emitted by the headless author script")
    ap.add_argument("--out", default=None)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    print(f"running ours on {args.instance}: 20N pop, Gmax={args.generations}, "
          f"{args.seeds} seed(s)", flush=True)
    ours = run_ours(args.instance, args.seeds, args.generations, not args.quiet)
    his = json.loads(Path(args.his).read_text()) if args.his else None
    report(ours, his)
    if args.out:
        payload = {"ours": ours, "his": his}
        Path(args.out).write_text(json.dumps(payload, indent=2))
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
