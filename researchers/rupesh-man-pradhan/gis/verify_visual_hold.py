#!/usr/bin/env python3
"""Fail-closed validation for an archival visual image, not a publication figure."""
from pathlib import Path
import json
p=Path(__file__).with_name("illustrative-map.v0.2.5-hold.json")
m=json.loads(p.read_text(encoding="utf-8"))
assert m["artifact_id"]=="RMP-GIS-V02_5-ILLUSTRATIVE-VISUAL-HOLD-20261015"
assert m["status"]=="PRESERVED_AS_ILLUSTRATIVE_REFERENCE__NOT_THESIS_VALIDATED"
assert m["publication_admitted"] is False and m["scientifically_verified"] is False
assert m["asset"]["source_media_class"]=="GENERATED_RASTER_ILLUSTRATION"
assert m["asset"]["local_byte_size"]==m["asset"]["drive_metadata_size_verified"]==1849811
assert len(m["asset"]["local_content_sha256"])==64
assert m["research_record"]["non_engineered_ok_filter"]=="NOT_VERIFIED_OR_APPLIED_TO_GENERATED_IMAGE"
assert m["figure_audit"]["nepal_shapefile_was_used"] is False
assert m["figure_audit"]["graticule_is_computationally_generated"] is False
assert m["figure_audit"]["scalebar_is_computationally_verified"] is False
assert m["figure_audit"]["point_positions_match_input_coordinates"] is False
assert m["governance"]["survey_coordinate_rows_in_public_git"] is False
print("PASS: V02.5 archived visual remains explicitly NOT FOR THESIS PUBLICATION")
