from __future__ import annotations

from pathlib import Path

import pdfplumber


FILES = [
    ("book_chapter", Path("/Users/aayushjha/Downloads/2022'Book Chapter-ContrainerTransport.pdf")),
    ("fsmj_journal", Path("/Users/aayushjha/Downloads/2023'FSMJ-Journal-AGVinCT.pdf")),
    ("xai_moo", Path("/Users/aayushjha/Downloads/Homayouni_XAI+MOO.pdf")),
]

OUTDIR = Path("tmp/pdfs/equation_extraction")


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    for name, path in FILES:
        with pdfplumber.open(path) as pdf:
            chunks: list[str] = []
            for i, page in enumerate(pdf.pages, 1):
                chunks.append(f"\n\n===== PAGE {i} =====\n")
                chunks.append(
                    page.extract_text(x_tolerance=1, y_tolerance=3, layout=True) or ""
                )
            (OUTDIR / f"{name}.txt").write_text("".join(chunks), encoding="utf-8")
            print(f"{name}: {len(pdf.pages)} pages")


if __name__ == "__main__":
    main()
