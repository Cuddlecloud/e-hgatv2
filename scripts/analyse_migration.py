"""Statistical analysis of bottleneck migration across the A/Q sweep.

Answers the thesis's core empirical question: does the binding bottleneck of a Pareto-optimal
schedule migrate between vehicle travel and crane handling as the front is traversed, and does
that migration depend on the fleet-to-crane ratio A/Q?

The measure is the **duration-weighted** critical share ``rho`` from
:mod:`ehgat.explain.critical_share`: of the total on-path duration that composes ``C_max``, the
fraction contributed by travel legs. ``rho_transport + rho_handling = 1`` by construction, and
``closes`` verifies that the on-path durations reproduce the makespan, so the measure cannot
drift from the objective it explains. Migration is the signed shift
``rho(energy end) - rho(makespan end)``.

Two things earlier analyses did not do, and this does:

1. **A hypothesis test rather than an interval.** Migration is tested against zero with a
   one-sample Wilcoxon signed-rank across seeds, with the matched-pairs rank-biserial effect
   size (Kerby 2014) and a percentile bootstrap CI of the median. Holm-Bonferroni corrects
   within each instance's family of fleet sizes, so nine simultaneous tests per instance cannot
   manufacture a significant one. All of this is reused from
   :mod:`ehgat.benchmark.stats`, not reimplemented.
2. **Separates the exact result from the model's.** The exact ``rho`` requires no network and is
   the required claim; the model's reproduction of it is reported alongside but never merged, so
   that the accuracy of the surrogate neither strengthens nor qualifies the exact finding.

Writes ``experiments/thesis/migration_stats.json`` and prints the table.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ehgat.benchmark.stats import holm_correction, wilcoxon_paired  # noqa: E402


def load(path: Path) -> list[dict]:
    return json.loads(path.read_text())["per_seed"]


def main() -> None:
    ap = argparse.ArgumentParser(description="Migration statistics over the A/Q sweep.")
    ap.add_argument("--sweep", type=Path,
                    default=Path("experiments/thesis/thesis_sweep540.json"))
    ap.add_argument("--out", type=Path, default=Path("experiments/thesis/migration_stats.json"))
    args = ap.parse_args()

    rows = load(args.sweep)
    print(f"[migration] {len(rows)} replicates from {args.sweep}")

    # Exclude replicates whose exact decomposition does not close. These are argmax *ties*: when
    # two chains attain the makespan exactly, the oracle splits the subgradient between them
    # (0.5 each) and the ``> 0.5`` on-path threshold then discards both, so the on-path durations
    # under-account for C_max. Any single argmax would be a valid subgradient; the averaged one is
    # not a valid selection for an additive decomposition. Rather than let a partial path distort
    # rho, such replicates are dropped and counted in the open here.
    kept, dropped = [], []
    for r in rows:
        (kept if r["behaviour"]["exact"]["decomposition_closes"] else dropped).append(r)
    if dropped:
        print(f"[migration] EXCLUDED {len(dropped)}/{len(rows)} replicate(s) with a non-closing "
              f"exact decomposition (argmax tie):")
        for r in dropped:
            print(f"             {r['instance']} seed={r['seed']} A={r['num_agvs']} "
                  f"Q={r['num_qcs']} A/Q={r['agv_per_qc']:.2f}")
    rows = kept

    # Group migration values by (instance, A/Q), keyed so seeds stay aligned for the paired test.
    groups: dict[tuple[str, float], dict[str, list[float]]] = defaultdict(
        lambda: {"exact": [], "model": [], "seed": [], "closes": []}
    )
    for r in rows:
        key = (r["instance"], round(r["agv_per_qc"], 4))
        b = r["behaviour"]
        groups[key]["exact"].append(float(b["exact"]["migration"]))
        groups[key]["model"].append(float(b["model"]["migration"]))
        groups[key]["seed"].append(int(r["seed"]))
        groups[key]["closes"].append(bool(b["exact"]["decomposition_closes"]))

    n_open = sum(1 for g in groups.values() for c in g["closes"] if not c)
    print(f"[migration] decomposition closes on {len(rows) - n_open}/{len(rows)} retained "
          f"replicates{' -- OK' if n_open == 0 else ' -- UNEXPECTED'}")

    # Test each (instance, A/Q) cell against zero migration, Holm-corrected within instance.
    by_instance: dict[str, list[tuple[float, dict]]] = defaultdict(list)
    for (inst, aq), g in sorted(groups.items()):
        exact = np.asarray(g["exact"], dtype=float)
        w = wilcoxon_paired(exact, np.zeros_like(exact), (f"{inst}@{aq}", "zero"))
        by_instance[inst].append((aq, {
            "aq": aq,
            "n_seeds": int(exact.size),
            "mean": float(exact.mean()),
            "median": float(np.median(exact)),
            "sd": float(exact.std(ddof=1)) if exact.size > 1 else 0.0,
            "pvalue": w.pvalue,
            "rank_biserial": w.rank_biserial,
            "ci_lo": w.ci_lo,
            "ci_hi": w.ci_hi,
            "model_mean": float(np.mean(g["model"])),
            "rho_abs_err": float(np.mean(np.abs(exact - np.asarray(g["model"], dtype=float)))),
        }))

    out: dict[str, object] = {
        "source": str(args.sweep),
        "n_replicates_retained": len(rows),
        "n_excluded_argmax_tie": len(dropped),
        "excluded": [{"instance": r["instance"], "seed": r["seed"],
                      "num_agvs": r["num_agvs"], "agv_per_qc": r["agv_per_qc"]} for r in dropped],
        "decomposition_mismatches_after_exclusion": n_open,
        "instances": {},
    }

    for inst, cells in by_instance.items():
        cells.sort(key=lambda c: c[0])
        holm = holm_correction([c[1]["pvalue"] for c in cells])
        for (_, cell), p in zip(cells, holm, strict=True):
            cell["pvalue_holm"] = p
            cell["significant"] = p < 0.05
        out["instances"][inst] = [c[1] for c in cells]

    print(f"\n{'inst':6}{'A/Q':>6}{'n':>4}{'migration':>11}{'sd':>8}"
          f"{'p(Holm)':>10}{'sig':>5}{'effect':>8}{'|exact-model|':>14}")
    for inst, cells in out["instances"].items():
        for c in cells:
            print(f"{inst:6}{c['aq']:6.2f}{c['n_seeds']:4d}{c['mean']:+11.3f}{c['sd']:8.3f}"
                  f"{c['pvalue_holm']:10.4f}{'*' if c['significant'] else '':>5}"
                  f"{c['rank_biserial']:+8.2f}{c['rho_abs_err']:14.5f}")

    # Headline: how many cells carry a significant non-zero migration, and where it peaks.
    all_cells = [(i, c) for i, cs in out["instances"].items() for c in cs]
    sig = [(i, c) for i, c in all_cells if c["significant"]]
    peak = max(all_cells, key=lambda ic: abs(ic[1]["mean"]))
    out["summary"] = {
        "cells": len(all_cells),
        "significant_cells": len(sig),
        "peak_instance": peak[0],
        "peak_aq": peak[1]["aq"],
        "peak_migration": peak[1]["mean"],
        "mean_abs_migration": float(np.mean([abs(c["mean"]) for _, c in all_cells])),
        "mean_rho_abs_error": float(np.mean([c["rho_abs_err"] for _, c in all_cells])),
    }
    print(f"\n[migration] {len(sig)}/{len(all_cells)} cells show significant non-zero migration "
          f"(Holm, alpha=0.05)")
    print(f"[migration] peak |migration| = {peak[1]['mean']:+.3f} at {peak[0]} A/Q={peak[1]['aq']:.2f}")
    print(f"[migration] mean |exact - model| rho error = {out['summary']['mean_rho_abs_error']:.5f}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2))
    print(f"[migration] wrote {args.out}")


if __name__ == "__main__":
    main()
