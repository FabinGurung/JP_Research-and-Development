#!/usr/bin/env python3
"""Restore only sha-verified non-Git assets from the frozen CP114 Drive ZIP.
No overwrite and no private fonts are accepted from this import path.
"""
from __future__ import annotations
import argparse, hashlib, json, zipfile
from pathlib import Path

def sha(p: Path):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):h.update(chunk)
    return h.hexdigest()

def main():
    root=Path(__file__).resolve().parents[1]
    p=argparse.ArgumentParser()
    p.add_argument('--source-zip',type=Path,required=True)
    args=p.parse_args()
    spec=json.loads((root/'binary-assets.manifest.json').read_text())
    if sha(args.source_zip)!=spec['source_archive_sha256']:
        raise SystemExit('SOURCE_ZIP_SHA256_MISMATCH — fail closed')
    count=0
    with zipfile.ZipFile(args.source_zip) as z:
        for a in spec['files']:
            rel=Path(a['path'])
            if rel.is_absolute() or '..' in rel.parts or rel.suffix.lower() in ('.ttf','.otf'):
                raise SystemExit('FORBIDDEN_PATH '+a['path'])
            target=root/rel
            if target.exists():
                if sha(target)!=a['sha256']:raise SystemExit('EXISTING_ASSET_DIFFERS: '+str(rel))
                continue
            b=z.read(rel.as_posix())
            if hashlib.sha256(b).hexdigest()!=a['sha256'] or len(b)!=a['bytes']:
                raise SystemExit('ASSET_HASH_MISMATCH '+str(rel))
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(b)
            count+=1
    print(f'PASS: verified {len(spec["files"])} assets; restored {count} new assets; no overwrite')
if __name__=='__main__':main()
