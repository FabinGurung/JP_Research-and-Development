#!/usr/bin/env python3
"""Static, source-only validation for Rupesh GIS V03.0; no private data in CI."""
from pathlib import Path
import ast
import hashlib
import json

p = Path(__file__).resolve().parent
m = json.loads((p / "all-wards-colored.v0.3.0.json").read_text(encoding="utf-8"))
b = (p / "RMP_GIS_V03_0_ALL_WARDS_COLOR_MAP.py").read_bytes()
src = b.decode("utf-8")
assert hashlib.sha256(b).hexdigest() == m["source_sha256"]
ast.parse(src)
assert m["version"] == "0.3.0" and m["parent_version"] == "0.2.7"
assert m["invariants"]["categorical_ward_fills"] == m["invariants"]["distinct_fill_colors"] == 33
assert m["invariants"]["rendered_points"] == 95
assert (m["invariants"]["rendered_engineered"], m["invariants"]["rendered_non_engineered"]) == (50,45)
assert m["invariants"]["non_ok_building_markers"] == 0
for k in ["geometry_changed","points_changed","filter_changed","extent_changed",
          "graticule_changed","scale_bar_changed","locator_changed"]:
    assert m["invariants"][k] is False
assert m["invariants"]["prior_ok_colors_preserved"] is True
assert "fc=ward_colors[w]" in src
assert "Ward colors (1–33)" in src
assert "else '#d8dcdf'" not in src
assert len(m["source_inputs_sha256"]) == 5
assert m["governance"]["raw_coordinates_in_public_git"] is False
assert m["qa"]["scientific_approval"] == "NOT_CLAIMED"
print("Rupesh V03.0: source hash, syntax, manifest and unchanged survey counts PASS.")
