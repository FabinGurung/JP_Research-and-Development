#!/usr/bin/env python3
"""Strict visual/text parity QA for a native Google Doc PDF export vs LaTeX PDF.

These two PDFs MUST be fetched from the actual provider and pinned to their IDs.
Never convert a Word draft to PDF and call that an authenticated Google Doc export.
"""
from __future__ import annotations
import argparse
from difflib import SequenceMatcher
import hashlib
import json
from pathlib import Path
import re

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def norm(text):
    return re.sub(r"\s+", " ", text).strip()

def compare(reference, native_export, dpi=100):
    try:
        import fitz
    except ImportError as e:
        raise SystemExit("PyMuPDF is required: pip install pymupdf") from e
    with fitz.open(reference) as a, fitz.open(native_export) as b:
        report = {
            "reference_sha256": sha256(reference),
            "native_doc_export_sha256": sha256(native_export),
            "reference_pages": len(a),
            "native_doc_export_pages": len(b),
            "page_count_pass": len(a) == len(b),
            "page_checks_completed": 0,
            "pages": [],
        }
        for i in range(min(len(a), len(b))):
            ta, tb = norm(a[i].get_text()), norm(b[i].get_text())
            similarity = SequenceMatcher(None, ta, tb, autojunk=False).ratio()
            x = a[i].get_pixmap(dpi=dpi, colorspace=fitz.csGRAY, alpha=False)
            y = b[i].get_pixmap(dpi=dpi, colorspace=fitz.csGRAY, alpha=False)
            geometry_equal = x.width == y.width and x.height == y.height
            identical = geometry_equal and x.samples == y.samples
            entry = {
                "page": i + 1,
                "text_similarity": round(similarity, 6),
                "pixel_identical": identical,
                "same_rendered_page_dimensions": geometry_equal,
                "pass": bool(identical and similarity == 1.0),
            }
            report["pages"].append(entry)
        report["page_checks_completed"] = len(report["pages"])
        report["failed_pages"] = [x["page"] for x in report["pages"] if not x["pass"]]
        report["overall_pass"] = report["page_count_pass"] and not report["failed_pages"]
        report["unpaired_reference_pages"] = list(range(len(b) + 1, len(a) + 1)) if len(a) > len(b) else []
        report["unpaired_doc_pages"] = list(range(len(a) + 1, len(b) + 1)) if len(b) > len(a) else []
        return report

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--reference", required=True, type=Path)
    p.add_argument("--native-export", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--dpi", type=int, default=100)
    a = p.parse_args()
    if not a.reference.is_file() or not a.native_export.is_file():
        p.error("Both source PDFs must exist")
    result = compare(a.reference, a.native_export, a.dpi)
    a.out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("PARITY_" + ("PASS" if result["overall_pass"] else "FAIL"),
          "reference:", result["reference_pages"],
          "doc:", result["native_doc_export_pages"],
          "failed paired pages:", len(result["failed_pages"]))
    raise SystemExit(0 if result["overall_pass"] else 1)

if __name__ == "__main__":
    main()
