import json
from pathlib import Path
m=json.loads(Path(__file__).with_name("ok-wards-survey-map.v0.2.7.json").read_text())
assert m["artifact_id"]=="RMP-GIS-V02_7-OK-WARD-SURVEY-POINT-MAP"
assert m["qa"]["plotted_total"]==95
assert m["qa"]["plotted_engineered"]+m["qa"]["plotted_non_engineered"]==95
assert m["qa"]["full_resolution_spatially_eligible"]==104
assert m["qa"]["held_due_to_display_boundary_precision"]==9
assert m["qa"]["ok_wards"]==[11,21,24,25,26,27,29,30,31,32,33]
assert m["coordinates_publicly_embedded"] is False
assert m["remaining_authority_gate"].startswith("Validate current official")
for h in [m["source_code_sha256"],m["map_png"]["sha256"],m["new_boundary_archive"]["sha256"]]:
    assert len(h)==64 and all(x in "0123456789abcdef" for x in h)
print("V02.7 manifest and public-code policy: PASS")
