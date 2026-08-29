"""Recompute every replicate whose critical-path decomposition failed to close.

All such failures predate the terminal-reduction correction in
:func:`ehgat.explain.tropical_dp.tropical_max`. The makespan was previously reduced with
``Tensor.max``, which divides the subgradient equally among tied maximisers, so a schedule
whose makespan is attained by two terminals attributed $1/2$ to each and the strict on-path
test admitted neither. The affected solves are reproduced from their recorded seed and fleet
size and only ``behaviour.exact`` is recomputed; all other fields are carried over unchanged.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))

THESIS = REPO / "experiments" / "thesis"


def _is_open(row: dict) -> bool:
    e = (row.get("behaviour") or {}).get("exact")
    if not e:
        return False
    mig = e.get("migration")
    return not e.get("decomposition_closes") or (isinstance(mig, float) and math.isnan(mig))


def _recompute(instance_id: str, seed: int, num_agvs: int | None, cfg: dict) -> dict:
    from run_thesis_experiments import _load

    from ehgat.baselines.mp_brkga import MpBRKGAConfig, run_mp_brkga
    from ehgat.environment.decoder import decode
    from ehgat.environment.evaluator import evaluate
    from ehgat.explain.critical_share import exact_critical_shares, migration

    instance = _load(instance_id, num_agvs)
    pop = cfg["pop_multiplier"] * instance.num_tasks
    t0 = time.perf_counter()
    res = run_mp_brkga(
        instance, MpBRKGAConfig(pop_size=pop, generations=cfg["generations"], seed=seed)
    )
    evaluated = sorted(
        ((decode(c, instance), None) for c in res.chromosomes),
        key=lambda pair: (lambda ev: (ev.makespan, ev.energy))(evaluate(pair[0], instance)),
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
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--files", nargs="+", required=True, help="thesis json basenames")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    for name in args.files:
        path = THESIS / f"{name}.json"
        doc = json.loads(path.read_text())
        cfg = doc["config"]
        rows = doc["per_seed"]
        targets = [r for r in rows if _is_open(r)]
        print(f"\n[{name}] {len(targets)} non-closing of {len(rows)}", flush=True)
        if args.dry_run:
            continue
        for row in targets:
            before = row["behaviour"]["exact"]
            after = _recompute(row["instance"], row["seed"], row.get("num_agvs"), cfg)
            print(f"  {row['instance']} seed={row['seed']} A={row.get('num_agvs')}: "
                  f"closes {before['decomposition_closes']} -> {after['decomposition_closes']}, "
                  f"mig {before['migration']} -> {after['migration']:.4f} "
                  f"({after['_repair_solve_s']:.0f}s)", flush=True)
            row["behaviour"]["exact"] = after
        doc.setdefault("_provenance", {})["nonclosing_repair"] = (
            f"{len(targets)} replicate(s) recomputed after the tropical terminal-reduction "
            "fix; solves reproduced from the recorded seed and fleet size."
        )
        path.write_text(json.dumps(doc, indent=2))
        print(f"[{name}] wrote {path}", flush=True)


if __name__ == "__main__":
    main()
