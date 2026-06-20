"""Command-line interface for tamil-ocr."""

import argparse
import json
import sys


def parse_pages(pages_str: str):
    """Parse '20,21,23' or '20-30' into a list of ints."""
    if "-" in pages_str and "," not in pages_str:
        start, end = pages_str.split("-", 1)
        return list(range(int(start), int(end) + 1))
    return [int(p.strip()) for p in pages_str.split(",")]


def main():
    parser = argparse.ArgumentParser(
        prog="tamil-ocr",
        description="OCR a Tamil PDF using Surya",
    )
    parser.add_argument("pdf", help="Path to PDF file")
    parser.add_argument(
        "--pages",
        help="Pages to extract: '20,21,23' or '20-30' (default: all)",
        default=None,
    )
    parser.add_argument(
        "--out",
        help="Write JSON output to file instead of stdout",
        default=None,
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=144,
        help="Render DPI (default: 144)",
    )
    parser.add_argument(
        "--illus-threshold",
        type=int,
        default=150,
        help="Char count below which a page is flagged as illustration (default: 150)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print progress to stderr",
    )

    args = parser.parse_args()

    pages = parse_pages(args.pages) if args.pages else None

    from tamil_ocr import ocr_pdf
    results = ocr_pdf(
        args.pdf,
        pages=pages,
        dpi=args.dpi,
        illustration_threshold=args.illus_threshold,
        verbose=args.verbose,
    )

    output = [
        {
            "page_num": r.page_num,
            "text": r.text,
            "char_count": r.char_count,
            "is_illustration": r.is_illustration,
        }
        for r in results
    ]

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"Written to {args.out}", file=sys.stderr)
    else:
        for r in output:
            if not r["is_illustration"]:
                print(f"\n--- Page {r['page_num']} ---")
                print(r["text"])


if __name__ == "__main__":
    main()
