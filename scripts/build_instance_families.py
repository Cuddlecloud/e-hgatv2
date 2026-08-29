"""Build the three published instance families on the same terminal layout.

Data set 1 is Table 5 of the book chapter as printed (loading). Data set 2 is the same data with
origins and destinations reversed (unloading), per Section 5.1. Data set 3 is the 26 dual-cycling
instances, each combining one unloading with one loading instance; the pairing is taken from the
``combination`` column of Table 3 (p. 177), read from
``data/Container_Transport_Parsed_Tables/container_transport_tables_1_to_5.json``.

Section 5.4 supplies the remaining detail: the two halves of a same-index pair such as U01&L01
describe one ship, so they share a quay-crane set, whereas a different-index pair describes two
ships served at once and the crane sets are disjoint. The published instances already number
their cranes in disjoint blocks, so combining them unmodified reproduces both cases. The build
asserts the resulting crane and task counts against the published Q-T column and refuses to write
if any of the 26 disagrees.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from ehgat.environment.dsdl import load_tables_4_5  # noqa: E402

PARSED = REPO / "data" / "Container_Transport_Parsed_Tables" / "container_transport_tables_1_to_5.json"
OUT = REPO / "data" / "instance_families.json"


def _tasks(inst, kind: str) -> list[dict]:
    return [{"qc": t.qc, "handling_time": float(t.handling_time), "lu": t.lu, "kind": kind}
            for t in inst.tasks]


def main() -> None:
    recs = {r.instance_id: r.instance for r in load_tables_4_5(str(REPO / "data" / "tables_4_5.json"))}
    t3 = json.loads(PARSED.read_text())["tables"]["table_3"]["rows"]

    fam: dict[str, dict] = {}
    for name, inst in recs.items():                       # data set 1
        fam[f"L_{name}"] = {"family": "loading", "source": "Table 5 as printed",
                            "tasks": _tasks(inst, "LOAD")}
    for name, inst in recs.items():                       # data set 2
        fam[f"U_{name}"] = {"family": "unloading",
                            "source": "Table 5 with origins and destinations reversed (Sec 5.1)",
                            "tasks": _tasks(inst, "UNLOAD")}

    bad = []
    for row in t3:                                        # data set 3
        ds = row["instance"]
        u, l = row["combination"].split("&")
        # U_n is L_n with the legs reversed, so the unloading half is built from L_n
        tasks = _tasks(recs[u.replace("U", "L")], "UNLOAD") + _tasks(recs[l], "LOAD")
        q_pub, t_pub = (int(x) for x in row["q_t"].split("-"))
        q, t = len({x["qc"] for x in tasks}), len(tasks)
        if (q, t) != (q_pub, t_pub):
            bad.append(f"{ds}={row['combination']}: built {q}-{t}, published {q_pub}-{t_pub}")
        fam[ds] = {"family": "mixed", "source": f"Table 3 comb. of = {row['combination']}",
                   "combination": row["combination"], "published_qt": row["q_t"],
                   "num_agvs_published": 2, "tasks": tasks}

    if bad:
        raise SystemExit("REFUSING to write; published Q-T mismatch:\n  " + "\n  ".join(bad))

    fam["_provenance"] = {
        "loading": "Table 5 as printed",
        "unloading": "Table 5 reversed, Sec 5.1",
        "mixed": "Table 3 'combination' column, all 26 verified against the published Q-T",
        "note": ("An earlier build paired consecutive identifiers, which is NOT the published "
                 "set: its task counts ran 8-32 where the published set has only 8, 12 and 16."),
    }
    OUT.write_text(json.dumps(fam, indent=2))
    n = {k: sum(1 for v in fam.values() if isinstance(v, dict) and v.get("family") == k)
         for k in ("loading", "unloading", "mixed")}
    print(f"wrote {OUT}: {n}")
    print(f"all 26 dual-cycling instances match the published Q-T column")


if __name__ == "__main__":
    main()
