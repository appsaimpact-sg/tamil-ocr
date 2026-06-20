"""Lazy-loaded Surya OCR wrapper."""

import os
import re

from PIL import Image

LLAMA_BIN = "/opt/homebrew/bin/llama-server"

_recognizer = None


def _get_recognizer():
    global _recognizer
    if _recognizer is None:
        # llama-server must be on PATH for Surya's backend
        if os.path.exists(LLAMA_BIN):
            os.environ.setdefault("LLAMA_CPP_BINARY", LLAMA_BIN)
        from surya.recognition import RecognitionPredictor
        _recognizer = RecognitionPredictor()
    return _recognizer


def ocr_image(image: Image.Image) -> str:
    """Run Surya OCR on a PIL image and return plain text."""
    rec = _get_recognizer()
    results = rec([image], full_page=True)
    texts = []
    for block in results[0].blocks:
        plain = re.sub(r"<[^>]+>", " ", block.html or "").strip()
        if plain:
            texts.append(plain)
    return "\n".join(texts)
