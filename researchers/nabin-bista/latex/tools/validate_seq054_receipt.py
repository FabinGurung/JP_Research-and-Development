#!/usr/bin/env python3
"""Nabin RSH-003: verify an *externally downloaded* SEQ054 PDF against release receipt.

This script checks structural/document facts; it does not certify engineering models.
Usage: python validate_seq054_receipt.py /path/to/seq054.pdf
"""
import pathlib, sys, json
import fitz
P=pathlib.Path(sys.argv[1]); doc=fitz.open(P)
sections=["General","Modal Characteristics","Response-Spectrum Storey Displacement","Response-Spectrum Inter-Storey Drift","Base Shear and Storey Shear","Foundation Settlement and Vertical Reaction","Beam and Column Force Envelopes","Preliminary X-Direction Fragility Assessment","Overall Discussion"]
text="\n".join(p.get_text() for p in doc)
checks={
  "77_A4_pages":len(doc)==77 and all(abs(p.rect.width-595.276)<1 and abs(p.rect.height-841.89)<1 for p in doc),
  "no_blank_pages":all(p.get_text().strip() for p in doc),
  "required_9_chapter4_headings":all(s in text for s in sections),
  "source_based_fragility_title": "Preliminary X-Direction Fragility Assessment" in text
}
print(json.dumps(checks,indent=2));sys.exit(0 if all(checks.values()) else 1)
