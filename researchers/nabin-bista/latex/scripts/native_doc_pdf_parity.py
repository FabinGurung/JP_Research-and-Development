#!/usr/bin/env python3
"""Source-PDF versus exported native-Google-Doc PDF parity report. Does not certify from counts alone."""
import json,re,sys
from pathlib import Path
from difflib import SequenceMatcher
import fitz

def norm(x):return re.sub(r"\s+"," ",x).strip().casefold()

def analyze(a,b):
    da=fitz.open(a);db=fitz.open(b)
    ta=[norm(p.get_text()) for p in da]
    tb=[norm(p.get_text()) for p in db]
    n=min(len(ta),len(tb))
    ratios=[SequenceMatcher(None,ta[i][:2400],tb[i][:2400]).ratio() for i in range(n)]
    return {
        "latex_pages":len(da),"native_doc_export_pages":len(db),
        "equal_page_counts":len(da)==len(db),
        "low_text_similarity_page_indices":[i+1 for i,x in enumerate(ratios) if x<.9],
        "reference_image_placements":sum(len(p.get_images(full=True)) for p in da),
        "native_image_placements":sum(len(p.get_images(full=True)) for p in db),
        "native_equation_and_table_structure":"NOT_INFERABLE_FROM_PDF__VERIFY_GOOGLE_DOCS_API_NATIVE_OBJECTS",
        "parity":"FAIL" if len(da)!=len(db) or any(x<.9 for x in ratios) else "VISUAL_QA_REQUIRED",
        "note":"This report is internal audit evidence. Never place it inside the submitted thesis."
    }
if __name__=="__main__":
    if len(sys.argv)!=4:raise SystemExit("usage: check.py latex.pdf native_export.pdf report.json")
    Path(sys.argv[3]).write_text(json.dumps(analyze(sys.argv[1],sys.argv[2]),indent=2))
