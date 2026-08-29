"""Append a JSON dump of the final Pareto front to each headless mp-BRKGA script.

His script prints only the two extreme points, with labels that are easy to misread (``ObjC``
holds ``[min Cmax, E at that point]`` while ``ObjE`` holds ``[min E, Cmax at that point]``).
Comparing fronts rather than parsing prose removes that ambiguity, so the dump writes the whole
front and both extremes, computed from ``BestObj`` directly rather than from his printed summary.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

DUMP = '''

# ---- JSON dump of the final front (added for the fidelity comparison) -------------------
if _out:
    import json as _json
    _front = [[float(_r[0]), float(_r[1])] for _r in np.asarray(BestObj)[:, :2]]
    _front.sort()
    _mk = min(_front, key=lambda p: (p[0], p[1]))
    _en = min(_front, key=lambda p: (p[1], p[0]))
    _json.dump(
        {
            "source": "author",
            "instance": _INSTANCE,
            "rep": REP,
            "gmax": Gmax,
            "nex": nex,
            "pop_max": int(Pmax),
            "n_tasks": int(N),
            "num_agvs": int(A),
            "num_qcs": int(I),
            "front": _front,
            "front_size": len(_front),
            "makespan_min": _mk[0],
            "energy_at_makespan_min": _mk[1],
            "energy_min": _en[1],
            "makespan_at_energy_min": _en[0],
            "gd_mean": float(ss.mean(GD)),
            "spread_mean": float(ss.mean(SP)),
            "time_mean": float(ss.mean(Time)),
        },
        open(_out, "w"),
        indent=2,
    )
    print("wrote", _out)
'''


def patch(path: Path, instance: str) -> None:
    text = path.read_text()
    if "JSON dump of the final front" in text:
        return
    text = text.replace('_out = _os.environ.get("MPB_OUT")',
                        f'_out = _os.environ.get("MPB_OUT")\n_INSTANCE = "{instance}"', 1)
    text = text + DUMP
    ast.parse(text)
    path.write_text(text)
    print(f"patched {path.name}")


if __name__ == "__main__":
    names = sys.argv[1:] or [f"DL{n:02d}" for n in range(1, 11)]
    for name in names:
        patch(Path(f"large/headless/mp_brkga_{name}_headless.py"), name)
