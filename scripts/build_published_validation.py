"""Compare the makespan-optimal end of the computed loading fronts against the published optima.

The artifact this writes, experiments/thesis/published_validation.json, previously had no
generator: it was produced once and read thereafter by make_thesis_tables.published_table().
When the small-set campaign was re-run at the scaled training budget the artifact kept the old
fronts, and thirteen of the thirty-five best makespans had moved, so Table 4.1 reported a
comparison against fronts the thesis no longer contains. Making the artifact reproducible is
what stops that recurring.

The published values are Table 1 of the book chapter (data set 1, the 35 loading instances).
Our runs select among three speeds per leg where each published scenario fixes one, so they
solve a less constrained problem and the computed makespan should lie at or below every
published column; a value above one indicates an evaluator error or a search shortfall.
"""

from __future__ import annotations

import argparse
import collections
import json
import statistics as st
from pathlib import Path

PUBLISHED = Path("data/Container_Transport_Parsed_Tables/container_transport_tables_1_to_5.json")

# The four published makespan columns, as (scenario, field) paths into a Table 1 row. The energy
# columns are not comparable: the speed selection can only reduce a makespan, whereas energy
# moves in either direction, so they are compared in the reconstruction check instead.
COLUMNS = (
    ("scenario_n", "c_max"),
    ("scenario_n", "c_max_star"),
    ("scenario_l_tilde_n", "c_max"),
    ("scenario_n_tilde_h", "c_max_star"),
)

NOTE = ("Our runs use the three-velocity Scenario 3, which yields a front and has no published "
        "column; the makespan-optimal end is compared against every fixed-speed column to "
        "establish which it corresponds to.")


def best_makespans(runs: Path) -> dict[str, float]:
    """Lowest makespan attained on each instance, over every seed of the campaign."""
    doc = json.loads(runs.read_text())
    rows = doc.get("per_seed", doc) if isinstance(doc, dict) else doc
    if isinstance(doc, dict) and "_SUPERSEDED" in doc:
        raise SystemExit(f"REFUSING to read superseded artifact {runs}: {doc['_SUPERSEDED']}")
    best: dict[str, float] = collections.defaultdict(lambda: float("inf"))
    for r in rows:
        best[r["instance"]] = min(best[r["instance"]], r["quality"]["mp_brkga"]["makespan_min"])
    return dict(best)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--runs", type=Path, default=Path("experiments/thesis/thesis_L_scaled.json"))
    ap.add_argument("--out", type=Path, default=Path("experiments/thesis/published_validation.json"))
    args = ap.parse_args()

    ours = best_makespans(args.runs)
    published = json.loads(PUBLISHED.read_text())["tables"]["table_1"]["rows"]

    results, blank = [], 0
    for row in published:
        inst = row["instance"]
        if inst not in ours:
            continue
        entry: dict[str, object] = {"instance": inst, "ours_makespan_min": ours[inst]}
        for scen, field in COLUMNS:
            key = f"{scen}.{field}"
            val = row.get(scen, {}).get(field)
            if val is None:                      # the authors' solver did not close this cell
                blank += 1
                continue
            entry[key] = val
            entry[f"{key}__gap"] = ours[inst] - val
        results.append(entry)

    summary = {}
    for scen, field in COLUMNS:
        key = f"{scen}.{field}"
        gaps = [r[f"{key}__gap"] for r in results if f"{key}__gap" in r]
        summary[key] = {
            "n_comparable": len(gaps),
            "n_exact": sum(1 for g in gaps if abs(g) < 1e-9),
            "n_at_or_below": sum(1 for g in gaps if g <= 1e-9),
            "mean_gap": st.mean(gaps),
            "median_gap": st.median(gaps),
        }

    args.out.write_text(json.dumps({
        "runs": str(args.runs),
        "published_source": str(PUBLISHED),
        "note": NOTE,
        "results": results,
        "summary": summary,
        "blank_cells_skipped": blank,
    }, indent=1))

    print(f"wrote {args.out}  from {args.runs}")
    for key, v in summary.items():
        print(f"  {key:<32} comparable={v['n_comparable']:>2}  at-or-below={v['n_at_or_below']:>2}  "
              f"exact={v['n_exact']}  mean gap={v['mean_gap']:+.2f}s")
    above = [(r["instance"], k[:-5], r[k]) for r in results for k in r
             if k.endswith("__gap") and r[k] > 1e-9]
    print(f"  cells above the published optimum: {len(above)}"
          + ("".join(f"\n    {i} {c} by {g:+.2f}s" for i, c, g in above) if above else ""))


if __name__ == "__main__":
    main()
