"""Transcription of the DL01--DL10 instances from the author's mp-BRKGA sources.

The ten reference implementations supplied by the author each carry their instance data as
module-level literals, so the geometry and task lists are recovered by parsing the assignment
nodes rather than by executing the files (which import IPython) or by retyping the numbers.
Every quantity below is read from those literals; nothing is inferred.

Two conventions are taken verbatim from the author's own unpacking loop. Each row of ``Data``
holds one quay crane's tasks as consecutive ``(Type, tau, LU)`` triples with ``Type`` 1 for a
loading and 0 for an unloading move, and only the first ``tasks`` triples of a row are read --
later rows carry unused trailing triples that the reference implementation skips. Node indices
are one-based in the source and the loading/unloading stations are offset by twenty, so raw
crane index ``x`` denotes ``QC{x}`` and raw station index ``x`` denotes ``LU{x}``.

The distance matrix is byte-identical across all ten sources and is written once. It describes a
twenty-crane, twenty-station terminal whose station return path is a one-way loop of
circumference 1150 m; it therefore differs from the twelve-node matrix of the published book
chapter in the station-to-station block, and the two are not interchangeable.
"""

from __future__ import annotations

import argparse
import ast
import csv
import json
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
DEFAULT_SRC = Path.home() / "Downloads" / "large"

NUM_QC_NODES = 20
NUM_LU_NODES = 20
LU_INDEX_OFFSET = 20  # the author's ``LU = [x - 1 + 20 for x in LU]``

_WANTED = ("Dis", "Data", "qc", "LAGV", "I", "tasks", "velocityE", "velocityL", "Scenario")


def _module_literals(path: Path, names: tuple[str, ...]) -> dict[str, Any]:
    """Top-level literal assignments of ``path``, keeping the first binding of each name.

    Only ``ast.literal_eval``-able right-hand sides are returned, so the parse is unaffected by
    the surrounding procedural code and no import of the source occurs.
    """
    tree = ast.parse(path.read_text())
    out: dict[str, Any] = {}
    for node in tree.body:
        if not (isinstance(node, ast.Assign) and len(node.targets) == 1):
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name) or target.id not in names or target.id in out:
            continue
        try:
            out[target.id] = ast.literal_eval(node.value)
        except (ValueError, SyntaxError):
            continue
    return out


def node_names() -> list[str]:
    """Ordered node names matching the author's index convention (cranes then stations)."""
    return [f"QC{i + 1}" for i in range(NUM_QC_NODES)] + [
        f"LU{k + 1}" for k in range(NUM_LU_NODES)
    ]


def _check_matrix(dis: list[list[float]]) -> None:
    """Fail loudly if the recovered matrix is not the expected square, non-negative loop."""
    size = NUM_QC_NODES + NUM_LU_NODES
    if len(dis) != size or any(len(row) != size for row in dis):
        raise ValueError(f"expected a {size}x{size} matrix, got {len(dis)} rows")
    if any(dis[i][i] != 0 for i in range(size)):
        raise ValueError("distance matrix has a non-zero diagonal")
    if any(v < 0 for row in dis for v in row):
        raise ValueError("distance matrix has a negative entry")
    circumferences = {
        dis[i][j] + dis[j][i]
        for i in range(LU_INDEX_OFFSET, size)
        for j in range(LU_INDEX_OFFSET, size)
        if i != j
    }
    if len(circumferences) != 1:
        raise ValueError(
            "station block is not a single one-way loop; "
            f"found circumferences {sorted(circumferences)}"
        )


def parse_instance(path: Path) -> tuple[dict[str, Any], list[list[float]]]:
    """Recover one DL record and its distance matrix from an mp-BRKGA source file."""
    lit = _module_literals(path, _WANTED)
    missing = [n for n in ("Dis", "Data", "qc", "LAGV", "I", "tasks") if n not in lit]
    if missing:
        raise ValueError(f"{path.name}: could not recover {missing}")

    num_qcs, per_qc = int(lit["I"]), int(lit["tasks"])
    data, cranes = lit["Data"], lit["qc"]
    if len(data) != num_qcs or len(cranes) != num_qcs:
        raise ValueError(f"{path.name}: I={num_qcs} disagrees with Data/qc lengths")

    tasks: list[dict[str, Any]] = []
    for i in range(num_qcs):
        row = data[i]
        if len(row) < per_qc * 3:
            raise ValueError(f"{path.name}: crane row {i} holds fewer than {per_qc} triples")
        for j in range(0, per_qc * 3, 3):
            kind_flag, tau, lu_raw = row[j], row[j + 1], row[j + 2]
            if kind_flag not in (0, 1):
                raise ValueError(f"{path.name}: unexpected Type {kind_flag!r}")
            tasks.append(
                {
                    "qc": f"QC{int(cranes[i])}",
                    "handling_time": float(tau),
                    "kind": "LOAD" if kind_flag == 1 else "UNLOAD",
                    "lu": f"LU{int(lu_raw)}",
                }
            )

    starts = {int(x) - 1 for x in lit["LAGV"]}
    if len(starts) != 1:
        raise ValueError(f"{path.name}: vehicles start at differing nodes {sorted(starts)}")
    start_index = starts.pop()
    if not LU_INDEX_OFFSET <= start_index < LU_INDEX_OFFSET + NUM_LU_NODES:
        raise ValueError(f"{path.name}: vehicle start index {start_index} is not a station")

    record = {
        "num_agvs": len(lit["LAGV"]),
        "agv_start": f"LU{start_index - LU_INDEX_OFFSET + 1}",
        "qcs": [f"QC{int(c)}" for c in cranes],
        "tasks": tasks,
        "_provenance": {
            "source": path.name,
            "num_qcs": num_qcs,
            "tasks_per_qc": per_qc,
            "scenario": int(lit.get("Scenario", -1)),
            "velocity_empty": float(lit.get("velocityE", float("nan"))),
            "velocity_loaded": float(lit.get("velocityL", float("nan"))),
        },
    }
    return record, lit["Dis"]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", type=Path, default=DEFAULT_SRC, help="directory of mp-BRKGA sources")
    ap.add_argument("--out-dir", type=Path, default=REPO / "data")
    args = ap.parse_args()

    sources = sorted(args.src.glob("mp-BRKGA_DL*.py"))
    if not sources:
        raise SystemExit(f"no mp-BRKGA_DL*.py under {args.src}")

    records: dict[str, Any] = {}
    matrices: dict[str, list[list[float]]] = {}
    for path in sources:
        instance_id = path.stem.split("_")[-1]
        record, dis = parse_instance(path)
        records[instance_id] = record
        matrices[json.dumps(dis)] = dis

    if len(matrices) != 1:
        raise SystemExit(f"sources disagree on the distance matrix ({len(matrices)} variants)")
    dis = next(iter(matrices.values()))
    _check_matrix(dis)

    names = node_names()
    matrix_path = args.out_dir / "dl_distance_matrix.csv"
    with matrix_path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["origin", *names])
        for origin, row in zip(names, dis, strict=True):
            writer.writerow([origin, *(int(v) if float(v).is_integer() else v for v in row)])

    json_path = args.out_dir / "dl_instances.json"
    payload = {
        "_provenance": (
            "Parsed from the author's mp-BRKGA_DL01..DL10 sources by "
            "scripts/transcribe_dl_instances.py. Distance matrix in dl_distance_matrix.csv "
            "(20 quay cranes by 20 loading/unloading stations, one-way station loop). "
            "Speed levels follow Scenario 3: time factors 1.25/1.0/0.83, empty power "
            "7.8/10/13.2 kW, loaded power 11.7/15/19.8 kW."
        ),
        **records,
    }
    json_path.write_text(json.dumps(payload, indent=2) + "\n")

    print(f"wrote {matrix_path.relative_to(REPO)} ({len(names)}x{len(names)})")
    print(f"wrote {json_path.relative_to(REPO)}")
    for instance_id, record in records.items():
        prov = record["_provenance"]
        print(
            f"  {instance_id}: N={len(record['tasks']):3d}  "
            f"QC={prov['num_qcs']:2d} x {prov['tasks_per_qc']:2d}  "
            f"AGV={record['num_agvs']}  start={record['agv_start']}"
        )


if __name__ == "__main__":
    main()
