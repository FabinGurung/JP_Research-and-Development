#!/usr/bin/env python3
"""Fail closed if a labelled, ADMITTED figure is missing from a release PDF.

Checks page and caption presence, not engineering model identity or scientific
approval. The original scientific data and Drive IDs must remain private.
"""
import argparse
import json
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--pdf", required=True, type=Path)
    ap.add_argument("--mode", choices=("preview","academic"), default="preview")
    args = ap.parse_args()
    import fitz
    data = json.loads(args.manifest.read_text())
    doc = fitz.open(args.pdf)
    failures = []
    if args.mode == "preview":
        if len(doc) != data.get("preview_pdf_pages"):
            failures.append("preview_page_count")
        for name, item in data.get("preview_expected_anchors", {}).items():
            n = item.get("preview_pdf_page")
            if not isinstance(n,int) or not (1<=n<=len(doc)) or len(doc[n-1].get_text().strip())<15:
                failures.append(name+":missing_preview_page")
        if sum(len(p.get_images(full=True)) for p in doc)<data.get("preview_image_xobjects",0):
            failures.append("lost_preview_image_objects")
    else:
        if data.get("academic_release","").startswith("NO_"):
            failures.append("academic_source_not_admitted")
        for item in data.get("items",[]):
            if item.get("admission_status")!="ADMITTED":
                continue
            n = item.get("academic_pdf_page")
            caption = item.get("academic_caption")
            tex = item.get("academic_latex_include")
            if not tex or not caption or not isinstance(n,int) or not (1<=n<=len(doc)):
                failures.append(str(item.get("asset"))+":missing_mapping")
            elif caption.casefold() not in doc[n-1].get_text().casefold():
                failures.append(str(item.get("asset"))+":caption_not_on_pdf_page")
        if data.get("science_release_conditions"):
            failures.append("open_scientific_release_holds")
    print(json.dumps({"mode":args.mode,"pdf_pages":len(doc),"passed":not failures,"failures":failures,"scientific_approval":False},indent=2))
    if failures:raise SystemExit(1)

if __name__=="__main__":
    main()
