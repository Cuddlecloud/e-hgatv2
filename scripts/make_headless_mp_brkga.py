"""Produce a headless, budget-overridable copy of the author's mp-BRKGA DL scripts.

His scripts are written for an IPython console: lines 12-13 import ``get_ipython`` and issue a
``%reset -sf`` magic, which raises outside IPython. Those two lines are the only obstacle to
running them unmodified, so they are removed and nothing else in the algorithm is touched.

A small shim makes ``REP``, ``Gmax`` and ``nex`` overridable from the environment, defaulting to
his published values, so the run can be timed at a reduced budget before the full one is
committed to. With no environment variables set the file reproduces his script exactly.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

SHIM = """
import os as _os
REP = int(_os.environ.get("MPB_REP", REP))
Gmax = int(_os.environ.get("MPB_GMAX", Gmax))
nex = int(_os.environ.get("MPB_NEX", nex))
_seed = _os.environ.get("MPB_SEED")
if _seed is not None:
    random.seed(int(_seed))
_out = _os.environ.get("MPB_OUT")
"""

ANCHOR = "rank= 0 #0: ranking using crowding distance 1: dominance"


def convert(src_path: Path, dst_path: Path) -> None:
    lines = src_path.read_text().split("\n")
    if "from IPython import get_ipython" not in lines[11]:
        raise SystemExit(f"{src_path}: line 12 is not the IPython import: {lines[11]!r}")
    if "get_ipython().magic" not in lines[12]:
        raise SystemExit(f"{src_path}: line 13 is not the reset magic: {lines[12]!r}")
    del lines[11:13]
    text = "\n".join(lines)
    if ANCHOR not in text:
        raise SystemExit(f"{src_path}: shim anchor not found")
    text = text.replace(ANCHOR, SHIM + "\n" + ANCHOR, 1)
    ast.parse(text)
    dst_path.write_text(text)
    print(f"{src_path.name} -> {dst_path} ({len(text.splitlines())} lines)")


if __name__ == "__main__":
    out_dir = Path("large/headless")
    out_dir.mkdir(parents=True, exist_ok=True)
    names = sys.argv[1:] or [f"DL{n:02d}" for n in range(1, 11)]
    for name in names:
        convert(Path(f"large/mp-BRKGA_{name}.py"), out_dir / f"mp_brkga_{name}_headless.py")
