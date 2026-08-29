"""Build the 26 dual-cycling instances exactly as the book chapter defines them.

The construction is taken from the source rather than inferred. Table 3 (p. 177) gives the pair
forming each instance in its "comb. of" column. Section 5.4 supplies the two details the pairing
alone does not: the AGVs are shared with two per instance, and whether the two halves share a
quay-crane set depends on whether they describe one ship or two -- a same-index pair such as
U01&L01 is a single ship being unloaded and then loaded, so both halves use the same QCs, while a
different-index pair is two ships served at once, so the QC sets are disjoint and the crane counts
add. Both facts are checked against the published Q-T column, which they reproduce on all 26.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from ehgat.environment.dsdl import load_tables_4_5  # noqa: E402


def main() -> None:
    tbl = json.loads((REPO / "data" / "ds_pairing_table3.json").read_text())
    recs = {r.instance_id: r for r in load_tables_4_5(str(REPO / "data" / "tables_4_5.json"))}

    out, report = {}, []
    for ds, (u, l) in sorted(tbl["pairs"].items()):
        lu_rec, ll_rec = recs[u.replace("U", "L")], recs[l]
        same_ship = u[1:] == l[1:]

        tasks = []
        # the unloading half: the loading task list with origin and destination reversed
        for t in lu_rec.instance.tasks:
            tasks.append({"qc": t.qc, "handling_time": float(t.handling_time),
                          "lu": t.lu, "kind": "UNLOAD"})
        # the loading half: shifted onto a disjoint QC set when the pair is two ships.
        # QC identifiers are strings ("QC3"), so the shift applies to the parsed index.
        shift = 0 if same_ship else len({t.qc for t in lu_rec.instance.tasks})
        for t in ll_rec.instance.tasks:
            qc = t.qc if not shift else f"QC{int(t.qc.removeprefix('QC')) + shift}"
            tasks.append({"qc": qc, "handling_time": float(t.handling_time),
                          "lu": t.lu, "kind": "LOAD"})

        q = len({t["qc"] for t in tasks})
        pub_q, pub_t = (int(x) for x in tbl["published_qt"][ds].split("-"))
        assert q == pub_q and len(tasks) == pub_t, f"{ds}: built {q}-{len(tasks)}, published {pub_q}-{pub_t}"
        out[ds] = {"family": "dual", "source": f"Table 3 comb. of = {u}&{l}",
                   "same_ship": same_ship, "num_agvs_published": tbl["agvs_published"],
                   "tasks": tasks}
        report.append((ds, f"{u}&{l}", f"{q}-{len(tasks)}", tbl["published_qt"][ds], "ok"))

    out["_provenance"] = {
        "pairing": "book chapter Table 3, 'comb. of' column",
        "construction": tbl["_construction"],
        "validation": "crane and task counts reproduce the published Q-T column on all 26",
    }
    dest = REPO / "data" / "ds_instances_table3.json"
    dest.write_text(json.dumps(out, indent=2))
    print(f"{'ins':<5}{'comb. of':<12}{'built':<8}{'published':<11}")
    for r in report:
        print(f"{r[0]:<5}{r[1]:<12}{r[2]:<8}{r[3]:<11}{r[4]}")
    print(f"\nwrote {dest} ({len(out)-1} instances, all matching published Q-T)")


if __name__ == "__main__":
    main()
