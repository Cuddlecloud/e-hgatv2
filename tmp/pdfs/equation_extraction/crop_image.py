from __future__ import annotations

from pathlib import Path

from PIL import Image


def crop(src: str, box: tuple[int, int, int, int], out: str) -> None:
    img = Image.open(src)
    img.crop(box).save(out)


crop(
    "tmp/pdfs/equation_extraction/book_page-11.png",
    (100, 420, 1250, 760),
    "tmp/pdfs/equation_extraction/book_page11_eq14_15_crop.png",
)
