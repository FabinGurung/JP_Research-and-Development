#!/usr/bin/env python3
"""Read-only, page-by-page PDF QA against the registered CURRENT Nabin Bista thesis."""
import argparse
import hashlib
import json
import unicodedata
from pathlib import Path

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--current", type=Path, required=True)
    ap.add_argument("--candidate", type=Path, required=True)
    ap.add_argument("--expected-pages", type=int, default=69)
    ap.add_argument("--dpi", type=float, default=72.0)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()
    try:
        import fitz
    except ImportError as ex:
        raise SystemExit("Requires PyMuPDF: pip install pymupdf") from ex
    original = fitz.open(args.current)
    rebuilt = fitz.open(args.candidate)
    wrong_pixels, wrong_text, wrong_geometry = [], [], []
    for i in range(min(len(original), len(rebuilt))):
        p, q = original[i], rebuilt[i]
        if tuple(p.rect) != tuple(q.rect):
            wrong_geometry.append(i + 1)
        v = fitz.Matrix(args.dpi / 72, args.dpi / 72)
        if p.get_pixmap(matrix=v, alpha=False).samples != q.get_pixmap(matrix=v, alpha=False).samples:
            wrong_pixels.append(i + 1)
        normalize = lambda t: unicodedata.normalize("NFKC", t).split()
        if normalize(p.get_text()) != normalize(q.get_text()):
            wrong_text.append(i + 1)
    result = {
        "schema": "NABIN-PDF-PARITY-001",
        "pass": len(original) == len(rebuilt) == args.expected_pages and not any((wrong_pixels, wrong_text, wrong_geometry)),
        "current_sha256": hashlib.sha256(args.current.read_bytes()).hexdigest(),
        "rebuilt_sha256": hashlib.sha256(args.candidate.read_bytes()).hexdigest(),
        "original_pages": len(original),
        "rebuilt_pages": len(rebuilt),
        "dpi": args.dpi,
        "pixels_different_pages": wrong_pixels,
        "text_different_pages": wrong_text,
        "page_geometry_different_pages": wrong_geometry,
        "binary_unchanged": args.current.read_bytes() == args.candidate.read_bytes(),
        "scientific_approval": False
    }
    print(json.dumps(result, indent=2))
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + "\n")
    if not result["pass"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
