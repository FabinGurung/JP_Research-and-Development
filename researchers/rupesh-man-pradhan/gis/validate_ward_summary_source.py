#!/usr/bin/env python3
"""Public-safe check of source-only Rupesh GIS V02.0 notebook metadata."""
import json, ast
from pathlib import Path
root=Path(__file__).resolve().parent
m=json.loads((root/"ward-summary.v0.2.0.json").read_text())
nb=json.loads((root/"RMP_GIS_V02_WARD_SUMMARY_SOURCE_ONLY.ipynb").read_text())
assert nb["nbformat"]==4
cells=nb["cells"]
assert len(cells)>=5
sources=[]
for cell in cells:
    if cell["cell_type"]=="code":
        assert not cell.get("outputs"),"Git source must have no Colab outputs"
        assert cell.get("execution_count") is None
        source="".join(cell["source"])
        ast.parse(source)
        sources.append(source)
combined="\n".join(sources)
for required in ["WARD_SOURCE_URL","SOURCE_DRIVE_CSV_ID","SOURCE_SPATIAL_CONFLICT","EPSG:32645","100000","RMP_GIS_M01__V01_4_SOURCE_BASELINE__2026-10-12"]:
    assert required in combined,required
assert "RMP-ENG-W33-R207" in combined
assert m["counts"]=={"survey_total":266,"engineered":150,"non_engineered":116,"spatial_qualified_wards":27,"source_qualified_wards":27,"spatial_vs_recorded_ward_conflicts":50,"manual_non_geometric_source_ward33":1}
assert m["a9_drive_sequence_advance"] is False
assert m["git_release_tag_for_this_edition"] is None
print("PASS: source-only GIS V02.0 notebook, pinned boundaries, QA caveats, Drive identifiers")
