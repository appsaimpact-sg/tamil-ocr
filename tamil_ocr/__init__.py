"""
tamil-ocr — Tamil PDF OCR using Surya

Usage:
    from tamil_ocr import ocr_pdf, ocr_image

    # All pages
    results = ocr_pdf("book.pdf")

    # Specific pages (1-based)
    results = ocr_pdf("book.pdf", pages=[20, 21, 23, 24])

    # Page range
    results = ocr_pdf("book.pdf", pages=(20, 30))

    # Single PIL image
    from PIL import Image
    text = ocr_image(Image.open("page.jpg"))

Each PageResult has: page_num, text, char_count, is_illustration
"""

from tamil_ocr._types import PageResult
from tamil_ocr._surya import ocr_image

import pathlib
import tempfile
from typing import Union

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


def ocr_pdf(
    pdf_path: Union[str, pathlib.Path],
    pages=None,
    dpi: int = 144,
    illustration_threshold: int = 150,
    verbose: bool = False,
) -> list:
    """
    OCR a PDF and return a list of PageResult objects.

    Args:
        pdf_path: path to the PDF file
        pages:    None (all pages), list of 1-based page numbers, or (start, end) tuple
        dpi:      render resolution (default 144)
        illustration_threshold: pages with fewer chars are flagged as illustrations
        verbose:  print progress to stdout

    Returns:
        list[PageResult]
    """
    if fitz is None:
        raise ImportError("PyMuPDF is required: pip install pymupdf")

    pdf_path = pathlib.Path(pdf_path)
    doc = fitz.open(str(pdf_path))
    total = doc.page_count

    # Resolve page list
    if pages is None:
        page_nums = list(range(1, total + 1))
    elif isinstance(pages, (tuple, list)) and len(pages) == 2 and isinstance(pages[0], int) and not isinstance(pages, list):
        # (start, end) range tuple
        start, end = pages
        page_nums = list(range(start, end + 1))
    else:
        page_nums = list(pages)

    scale = dpi / 72.0
    mat = fitz.Matrix(scale, scale)
    results = []

    for page_num in page_nums:
        if page_num < 1 or page_num > total:
            continue

        page = doc.load_page(page_num - 1)  # 0-based
        pix = page.get_pixmap(matrix=mat)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tf:
            tmp = tf.name
        pix.save(tmp)

        from PIL import Image as _Image
        img = _Image.open(tmp)
        text = ocr_image(img)

        import os
        os.unlink(tmp)

        char_count = len(text.strip())
        is_illus = char_count < illustration_threshold

        if verbose:
            label = "illustration" if is_illus else f"{char_count} chars"
            print(f"  p{page_num:03d}: {label}", flush=True)

        results.append(PageResult(
            page_num=page_num,
            text=text,
            char_count=char_count,
            is_illustration=is_illus,
        ))

    doc.close()
    return results


__all__ = ["ocr_pdf", "ocr_image", "PageResult"]
