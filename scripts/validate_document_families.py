#!/usr/bin/env python3
"""Regression test for the two-family R&D portal and no-delete template register."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def read(p):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))

def validate():
    router=read("controls/family-router.v0.1.json")
    assert router["primary_navigation"]==["home","enterprise-documents","academic-writing"]
    acad=read("controls/academic-writing/tower.json")
    ent=read("controls/document-engineering/tower.json")
    assert acad["control_id"]!=ent["id"]
    assert acad["family_id"]=="academic"
    assert (ROOT/"controls/latex/tower.json").is_file()
    assert (ROOT/"controls/presentation/tower.json").is_file()
    assert all((ROOT/child["canonical_control"]).is_file() for child in acad["children"])
    assert all(x!="controls/document-engineering/tower.json" for x in (child["canonical_control"] for child in acad["children"]))
    nav=read("registry/academic-family-navigation.v0.1.json")
    links=[item["route"] for group in nav["groups"] for item in group["items"]]
    assert len(links)==len(set(links)), "Academic navigation contains duplicated routes"
    assert all(route and ".." not in route for route in links)
    aud=read("registry/enterprise-template-normalization-audit.v0.1.json")
    reg=read("registry/enterprise-document-types.v2.json")["types"]
    assert len(aud["canonical"])==len(reg)==14
    assert {x["type_id"] for x in aud["canonical"]}=={x["id"] for x in reg}
    assert all((ROOT/x["path"]).is_file() for x in aud["canonical"])
    assert all((ROOT/x["path"]).is_file() for x in aud["overlaps"] if "branch" not in x)
    assert all(x["decision"]=="PENDING_USER_QA" for x in aud["overlaps"])
    assert all(x["production_approved"] is False for x in aud["canonical"])
    request=read("schemas/ai-job-request.v0.1.schema.json")
    assert request["properties"]["family_id"]["enum"]==["enterprise","academic"]
    return len(links)

if __name__=="__main__":
    links=validate()
    print(f"PASS two separate towers, 14 canonical templates, preserved legacy versions, {links} academic navigation entries")
