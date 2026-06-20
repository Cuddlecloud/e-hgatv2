from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader


FILES = [
    ("book_pypdf", Path("/Users/aayushjha/Downloads/2022'Book Chapter-ContrainerTransport.pdf")),
    ("xai_pypdf", Path("/Users/aayushjha/Downloads/Homayouni_XAI+MOO.pdf")),
]


for name, path in FILES:
    reader = PdfReader(path)
    print(name, len(reader.pages))
    for i, page in enumerate(reader.pages[:8], 1):
        text = page.extract_text() or ""
        print("PAGE", i, repr(text[:700]))
