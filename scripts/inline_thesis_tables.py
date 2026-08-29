"""Inline the \\input table fragments into main.tex, producing a single self-contained document.

Overleaf selects a compile target by scanning the project for candidate documents. The files in
``thesis/tables/`` are fragments intended for ``\\input`` and are not compilable in isolation, so
their presence causes Overleaf to attempt them as documents and emit hundreds of spurious errors.
Inlining them leaves exactly one ``.tex`` file in the project, which removes the ambiguity.

The generated fragments remain on disk and ``scripts/make_thesis_tables.py`` continues to write
them, so the tables are still produced from the experiment JSON rather than by hand; this script is
the final assembly step and is re-run whenever the tables are regenerated.

The step is idempotent. On the first run it replaces each ``\\input{tables/X}`` marker; on every
later run it replaces the block between the BEGIN/END provenance comments it wrote previously.
Without the second path a regenerated table would sit on disk and never reach the document, which
is exactly how a corrected caption can fail to appear in the compiled PDF.
"""

import re
from pathlib import Path

THESIS = Path("thesis/main.tex")
TABLES = Path("thesis/tables")
NAMES = ("traversal", "dl", "migration", "calibration", "smallset", "published", "validation",
         "families")


def main() -> None:
    text = THESIS.read_text()
    fresh = updated = 0

    for name in NAMES:
        fragment = (TABLES / f"{name}.tex").read_text().rstrip("\n")
        block = (f"% ---- BEGIN generated: tables/{name}.tex "
                 f"(scripts/make_thesis_tables.py) ----\n"
                 f"{fragment}\n"
                 f"% ---- END generated: tables/{name}.tex ----")

        marker = f"\\input{{tables/{name}}}"
        if marker in text:
            text = text.replace(marker, block, 1)
            fresh += 1
            continue

        # Already inlined: replace everything between the provenance comments.
        pattern = re.compile(
            re.escape(f"% ---- BEGIN generated: tables/{name}.tex")
            + r".*?"
            # consume the trailing dashes as well: without this the previous marker's tail
            # survives each replacement and another " ----" accumulates on every run
            + re.escape(f"% ---- END generated: tables/{name}.tex")
            + r"[ -]*",
            re.DOTALL,
        )
        text, n = pattern.subn(lambda _m: block, text, count=1)
        if n:
            updated += 1
        else:
            print(f"  warning: no marker and no generated block for tables/{name}.tex")

    THESIS.write_text(text)
    print(f"inlined {fresh} fragment(s), refreshed {updated} already-inlined block(s) "
          f"in {THESIS}")


if __name__ == "__main__":
    main()
