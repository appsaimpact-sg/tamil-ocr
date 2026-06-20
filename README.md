# tamil-ocr

Tamil PDF OCR using [Surya](https://github.com/VikParuchuri/surya) — purpose-built for Tamil script, much better accuracy than general vision LLMs.

## Install

```bash
pip install git+https://github.com/appsaimpact/tamil-ocr.git
```

**Requires `llama-server`** (Surya's backend):
```bash
brew install llama.cpp
```

## Python API

```python
from tamil_ocr import ocr_pdf, ocr_image

# All pages
results = ocr_pdf("book.pdf")

# Specific pages (1-based)
results = ocr_pdf("book.pdf", pages=[20, 21, 23, 24])

# Page range
results = ocr_pdf("book.pdf", pages=(20, 30))

for r in results:
    if not r.is_illustration:
        print(f"Page {r.page_num}: {r.text[:100]}")

# Single image
from PIL import Image
text = ocr_image(Image.open("page.jpg"))
```

### `PageResult` fields

| Field | Type | Description |
|---|---|---|
| `page_num` | `int` | 1-based page number |
| `text` | `str` | OCR plain text |
| `char_count` | `int` | `len(text.strip())` |
| `is_illustration` | `bool` | True if char_count < threshold (default 150) |

### `ocr_pdf` options

| Arg | Default | Description |
|---|---|---|
| `pages` | `None` (all) | List of page numbers or `(start, end)` tuple |
| `dpi` | `144` | Render resolution |
| `illustration_threshold` | `150` | Pages below this char count are flagged as illustrations |
| `verbose` | `False` | Print page-by-page progress |

## CLI

```bash
# All pages, print text to stdout
tamil-ocr book.pdf

# Specific pages
tamil-ocr book.pdf --pages 20,21,23,24

# Page range, save to JSON
tamil-ocr book.pdf --pages 20-30 --out output.json --verbose
```
