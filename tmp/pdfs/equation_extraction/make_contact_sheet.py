from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


def make_sheet(prefix: str, start: int, end: int, out: str) -> None:
    paths = [Path(f"tmp/pdfs/equation_extraction/{prefix}-{i:02d}.png") for i in range(start, end + 1)]
    thumbs: list[Image.Image] = []
    for p in paths:
        img = Image.open(p).convert("RGB")
        img.thumbnail((360, 500))
        canvas = Image.new("RGB", (380, 540), "white")
        canvas.paste(img, ((380 - img.width) // 2, 30))
        d = ImageDraw.Draw(canvas)
        d.text((10, 8), p.stem, fill="black")
        thumbs.append(canvas)
    cols = 4
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 380, rows * 540), "white")
    for idx, thumb in enumerate(thumbs):
        x = (idx % cols) * 380
        y = (idx // cols) * 540
        sheet.paste(thumb, (x, y))
    sheet.save(out)


make_sheet("book_page", 1, 16, "tmp/pdfs/equation_extraction/book_contact_01_16.png")
make_sheet("book_page", 17, 31, "tmp/pdfs/equation_extraction/book_contact_17_31.png")
