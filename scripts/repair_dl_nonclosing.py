"""Recompute the two DL replicates whose critical-path decomposition failed to close.

Both failures predate the terminal-reduction correction in :func:`tropical_max`: the
makespan was reduced with ``Tensor.max``, which divides the subgradient equally among
tied maximisers, so a schedule whose makespan is attained by two terminals attributed
$1/2$ to each and the strict on-path test admitted nothing. The solve is reproduced from
the recorded seed and configuration and only ``behaviour.exact`` is recomputed; every
other field of the record is carried over unchanged.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

TARGETS = {("DL01", 3), ("DL07", 2)}
FULL = REPO / "experiments" / "thesis" / "thesis_DL_full.json"


def _rerun(instance_id: str, seed: int, cfg: dict) -> dict:
    from ehgat.baselines.mp_brkga import MpBRKGAConfig, run_mp_brkga
    from ehgat.environment.decoder import decode
    from ehgat.environment.dsdl import load_dl_instances
    from ehgat.explain.critical_share import exact_critical_shares, migration

    instance = load_dl_instances(only=[instance_id])[0].instance
    pop = cfg["pop_multiplier"] * instance.num_tasks
    t0 = time.perf_counter()
    res = run_mp_brkga(
        instance, MpBRKGAConfig(pop_size=pop, generations=cfg["generations"], seed=seed)
    )
    schedules = [decode(c, instance) for c in res.chromosomes]

    from ehgat.environment.evaluator import evaluate

    evaluated = sorted(
        ((s, evaluate(s, instance)) for s in schedules),
        key=lambda pair: (pair[1].makespan, pair[1].energy),
    )
    mk = exact_critical_shares(evaluated[0][0], instance)
    en = exact_critical_shares(evaluated[-1][0], instance)
    return {
        "rho_makespan_end": mk.transport,
        "rho_energy_end": en.transport,
        "migration": migration(mk, en),
        "decomposition_closes": bool(mk.closes and en.closes),
        "_repair_solve_s": time.perf_counter() - t0,
    }


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--instance", required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--out", type=Path, required=True, help="single-replicate patch file")
    args = ap.parse_args()

    cfg = json.loads(FULL.read_text())["config"]
    after = _rerun(args.instance, args.seed, cfg)
    print(f"[repair] {args.instance} seed={args.seed}: "
          f"closes={after['decomposition_closes']} mig={after['migration']:.4f} "
          f"({after['_repair_solve_s']:.0f}s)", flush=True)
    args.out.write_text(json.dumps(
        {"instance": args.instance, "seed": args.seed, "exact": after}, indent=2))
    print(f"[repair] wrote {args.out}")


if __name__ == "__main__":
    main()
