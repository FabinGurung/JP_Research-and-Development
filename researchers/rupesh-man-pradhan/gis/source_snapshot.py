#!/usr/bin/env python3
"""Validate the candidate milestone; optionally create an output-free notebook copy.
Do not ingest or publish researcher coordinate records on public CI.
"""
import argparse
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
MANIFEST = BASE / "milestone.v0.1.4.json"

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def check_manifest() -> dict:
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert m["id"] == "RMP-GIS-MILESTONE-20261012-V01_4"
    assert m["release_tag"] == "rupesh-gis/v0.1.4-preview"
    assert m["release_class"] == "QA_CANDIDATE_NOT_SCIENTIFIC_APPROVAL"
    assert m["counts"] == {"input_records":266,"engineered":150,"non_engineered":116,"pokhara_display":265,"held_outliers":1}
    assert m["qa"]["live_tile_fetch"] == "UNVERIFIED_IN_USER_BROWSER"
    assert m["source"]["source_only_notebook_git_status"].startswith("NOT_YET_COMMITTED")
    assert m["privacy"]["raw_coordinate_records_in_public_git"] is False
    for k in ["original_spreadsheet_sha256","notebook_sha256_with_outputs",
              "source_only_notebook_sha256_after_stripping_outputs_and_normalizing_metadata"]:
        h = m["source"][k]
        assert len(h) == 64 and all(c in "0123456789abcdef" for c in h)
    assert m["history"]["routine_a9_local_main_seq_increment"] is False
    return m

def sanitize(infile: Path, outfile: Path, manifest: dict) -> None:
    raw = infile.read_bytes()
    assert sha256(raw) == manifest["source"]["notebook_sha256_with_outputs"], "Wrong Drive notebook version"
    book = json.loads(raw)
    for cell in book["cells"]:
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
    book.setdefault("metadata", {})["rmp_gis_version"] = "GIS-V01.4"
    book["metadata"]["map_engine"] = "Inline JavaScript with optional Esri/OSM raster tiles and explicit failure QA"
    clean = (json.dumps(book, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    assert sha256(clean) == manifest["source"]["source_only_notebook_sha256_after_stripping_outputs_and_normalizing_metadata"], "Sanitized source hash mismatch"
    outfile.write_bytes(clean)
    print("Clean source-only notebook:", outfile, "SHA-256:", sha256(clean))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook", nargs="?", type=Path, help="Original downloaded Drive .ipynb")
    parser.add_argument("--output", type=Path, default=Path("RMP_GIS_V01_4_SOURCE_CLEAN.ipynb"))
    args = parser.parse_args()
    m = check_manifest()
    if args.notebook:
        sanitize(args.notebook, args.output, m)
    print("GIS milestone manifest QA: PASS (external tiles and scientific approvals still unverified)")
