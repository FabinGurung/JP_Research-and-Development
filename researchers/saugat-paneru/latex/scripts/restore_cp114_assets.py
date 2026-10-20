#!/usr/bin/env python3
"""Verify / restore CP114 research assets into a Git checkout (RSH-002 only).

The Git repository intentionally holds editable LaTeX text, NOT the 143 binary
research assets. Pass the original, privately held approved CP114 source ZIP,
identified by its SHA-256; this script never downloads or publishes assets.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "asset-manifest-cp114.json"
DEFAULT_DEST = ROOT / "manuscript"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-zip", type=Path, help="Approved CP114 source ZIP from governed Drive")
    parser.add_argument("--root", type=Path, default=DEFAULT_DEST, help="Destination manuscript working directory")
    parser.add_argument("--check", action="store_true", help="Verify all assets without writing; use before every build")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    hashes = manifest["asset_file_sha256"]
    if manifest["asset_count"] != 143 or len(hashes) != 143:
        parser.error("Expected exactly 143 separately hashed CP114 assets.")
    target = args.root.resolve()
    if not target.is_dir():
        parser.error(f"Missing manuscript working directory: {target}")
    if not args.check and not args.source_zip:
        parser.error("Restoration requires --source-zip <approved CP114 zip>")
    if args.source_zip:
        source = args.source_zip.resolve()
        if not source.is_file():
            parser.error(f"Original CP114 ZIP does not exist: {source}")
        if file_hash(source) != manifest["original_cp114_source_zip_sha256"]:
            parser.error("CP114 source archive SHA-256 mismatch. Refusing all asset mutations.")
    missing, mismatch = [], []
    for name, expected in hashes.items():
        rel = Path(name)
        if rel.is_absolute() or ".." in rel.parts or rel.parts[0] not in ("figures", "assets", "appendices", "data"):
            parser.error(f"Unsafe or unexpected asset path: {name}")
        dest = target / rel
        if dest.is_symlink():
            parser.error(f"Symlink asset blocked: {dest}")
        if dest.exists():
            if not dest.is_file() or file_hash(dest) != expected:
                mismatch.append(name)
        else:
            missing.append(name)
    if mismatch:
        parser.error("Existing assets do not match frozen CP114: " + ", ".join(mismatch[:8]))
    if args.check:
        if missing:
            print(f"Missing {len(missing)}/143 CP114 binary source assets, including: {', '.join(missing[:4])}", file=sys.stderr)
            print(f"Restore with: python3 {Path(__file__).name} --source-zip /path/to/CP114_FINAL_TNR_SOURCE__20261007.zip", file=sys.stderr)
            return 3
        print(json.dumps({"status": "PASS", "verified": 143, "missing": 0, "mutated": 0}))
        return 0
    restored = 0
    with zipfile.ZipFile(source) as archive:
        members = set(archive.namelist())
        absent = [name for name in missing if name not in members]
        if absent:
            parser.error("Verified CP114 ZIP lacks expected manifest entries: " + ", ".join(absent[:8]))
        for name in missing:
            contents = archive.read(name)
            if sha256(contents) != hashes[name]:
                parser.error(f"Asset SHA-256 mismatch within approved ZIP: {name}")
            dest = target / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists() or dest.is_symlink():
                parser.error(f"Destination appeared during restore, refusing overwrite: {dest}")
            with tempfile.NamedTemporaryFile(dir=dest.parent, prefix=".cp114-asset-", delete=False) as tmp:
                tmp.write(contents)
                tmp_path = Path(tmp.name)
            if dest.exists() or dest.is_symlink():
                tmp_path.unlink()
                parser.error(f"Destination appeared before finalize: {dest}")
            os.replace(tmp_path, dest)
            restored += 1
    for name, expected in hashes.items():
        if file_hash(target / name) != expected:
            parser.error(f"Post-restore verification failed: {name}")
    print(json.dumps({"status": "PASS", "verified": 143, "restored": restored, "preexisting": 143 - restored}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
