#!/usr/bin/env python3
"""Fail-closed Safal LaTeX source gate; this is not a PDF compiler or uploader."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
d=json.loads((root/"controls/projects/safal-dawadi.latex.json").read_text(encoding="utf-8"))
assert d["researcher_id"]=="RSH-010"
g=d["gates"]
p=root/d["build"]["source_root"]/"manuscript/main.tex"
if g["source_admission"]!="VERIFIED" or g["source_reconciliation"]!="VERIFIED" or g["public_git_clearance"]!="VERIFIED":
    print("SAFAL_SOURCE_GATE: HOLD_NOT_ADMITTED; NO_PDF_COMPILED; NO_DRIVE_UPLOAD")
elif not p.is_file():
    raise SystemExit("SAFAL_SOURCE_GATE: ERROR_ADMITTED_SOURCE_MISSING")
else:
    print("SAFAL_SOURCE_GATE: SOURCE_PRESENT; EXACT_FONT_COMPILATION_NOT_ENABLED")
