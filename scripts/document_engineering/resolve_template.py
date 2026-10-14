#!/usr/bin/env python3
"""Unambiguous A9 enterprise template-name router.

A named template always resolves to exactly one current v3 source.
Older .tex files remain addressable only by explicit historical Git ref, not this router.
"""
import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
CANONICAL=ROOT/"registry/enterprise-document-types.json"
CLEAN=re.compile(r"[^a-z0-9]+")

def key(name):
    if not isinstance(name,str) or not name.strip():
        raise ValueError("Template name must be non-empty text")
    return CLEAN.sub(" ",unicodedata.normalize("NFKC",name).casefold()).strip()

def catalog():
    registry=json.loads(CANONICAL.read_text(encoding="utf-8"))
    records=registry["templates"]
    if registry.get("version")!="3.0.0" or len(records)!=14:
        raise ValueError("Active registry must have exactly 14 approved v3 entries")
    index={}
    for record in records:
        rid=record["id"]
        if record.get("path")!=f"templates/enterprise/v3/{rid}.tex":
            raise ValueError("Canonical template path mismatch: "+rid)
        if record.get("layout_qa_approved") is not True:
            raise ValueError("Canonical entry is not approved: "+rid)
        if not (ROOT/record["path"]).is_file():
            raise ValueError("Missing canonical TeX: "+rid)
        names=[rid,record["title"],*record.get("aliases",[])]
        for alias in names:
            k=key(alias)
            if k in index and index[k]["id"]!=rid:
                raise ValueError("Ambiguous name collision: "+alias)
            index[k]=record
    if len({r["path"] for r in records})!=14 or len({r["id"] for r in records})!=14:
        raise ValueError("Duplicate canonical IDs or source paths")
    return records,index

def resolve(name):
    _,index=catalog()
    found=index.get(key(name))
    if found is None:
        raise ValueError("Unregistered or ambiguous template name; no legacy fallback: "+name)
    return found

def selftest():
    records,index=catalog()
    assert len(records)==14 and len(index)>=14
    for entry in records:
        assert resolve(entry["id"])["id"]==entry["id"]
        assert resolve(entry["title"])["path"]==entry["path"]
        for alias in entry.get("aliases",[]):
            assert resolve(alias)["id"]==entry["id"]
    for bad in ("contract","letter","estimate old","works_contract.tex"):
        try:resolve(bad)
        except ValueError:pass
        else:raise AssertionError("Unsafe silent historical fallback: "+bad)
    print(f"PASS 14 canonical callable types, {len(index)} collision-free names, zero legacy fallbacks")

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--name")
    ap.add_argument("--list",action="store_true")
    ap.add_argument("--self-test",action="store_true")
    args=ap.parse_args()
    if args.self_test:selftest()
    elif args.list:
        records,_=catalog()
        print(json.dumps([{"id":r["id"],"title":r["title"],"template":r["path"]} for r in records],indent=2))
    elif args.name:
        r=resolve(args.name)
        print(json.dumps({"canonical_id":r["id"],"template":r["path"],"engine":"scripts/document_engineering/engine_v3.py","registry_version":"3.0.0"},indent=2))
    else:ap.error("Use --name, --list or --self-test")
