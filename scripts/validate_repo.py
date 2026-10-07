#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, re, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
errors=[]
def load(p):
    try:return json.loads((ROOT/p).read_text(encoding="utf-8"))
    except Exception as e: errors.append(f"{p}: {e}"); return {}
researchers=load("registry/researchers.json")
branches=load("registry/branch-registry.json")
policy=load("controls/repository.control.json")
required=["README.md","CURRENT.json","A7_MODULE.json","registry/researchers.json","registry/branch-registry.json","controls/repository.control.json","controls/discussion.control.json","controls/latex.control.json","controls/presentation.control.json","schemas/researchers.schema.json","scripts/build_site.py","scripts/validate_repo.py","web/styles.css",".github/workflows/validate.yml",".github/workflows/pages.yml"]
for p in required:
    if not (ROOT/p).is_file(): errors.append(f"missing {p}")
rows=researchers.get("researchers",[])
if len(rows)!=9: errors.append(f"expected 9 researchers, got {len(rows)}")
ids=set(); slugs=set(); lane_names=set()
for r in rows:
    if r.get("researcher_id") in ids: errors.append("duplicate researcher_id")
    if r.get("slug") in slugs: errors.append("duplicate slug")
    ids.add(r.get("researcher_id")); slugs.add(r.get("slug"))
    if r.get("qa_status")!="HOLD_HUMAN_QA": errors.append(f"{r.get('slug')}: not on QA hold")
    if r.get("topic_title") is not None or r.get("topic_short_name") is not None: errors.append(f"{r.get('slug')}: topic published before QA")
    for kind in ("discussion","latex","presentation"):
        b=r.get("lanes",{}).get(kind,{}).get("branch")
        exp=f"researcher/{r.get('slug')}/{kind}"
        if b!=exp: errors.append(f"{r.get('slug')}: {kind} branch mismatch")
        if b in lane_names: errors.append(f"duplicate lane {b}")
        lane_names.add(b)
if len(lane_names)!=27: errors.append("expected 27 researcher lanes")
reg={x.get("branch") for x in branches.get("active_researcher_lanes",[])}
if reg!=lane_names: errors.append("branch registry active lanes != researcher registry")
if len(branches.get("archived_legacy",[]))!=45: errors.append("expected 45 original non-main legacy refs")
if policy.get("repository_role")!="R_AND_D_CODE_POINTER_AND_CONTROL_PORTAL": errors.append("repository policy role mismatch")
# Main/lane binary guard. Git history may contain binaries; current tree may not.
try:
    files=subprocess.check_output(["git","ls-files"],cwd=ROOT,text=True).splitlines()
except Exception:
    files=[str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file()]
forbidden={".pdf",".pptx",".docx",".xlsx",".xls",".png",".jpg",".jpeg",".gif",".webp",".zip",".7z",".rar",".glb",".obj",".ifc",".dwg",".dxf"}
bad=[f for f in files if Path(f).suffix.lower() in forbidden]
if bad: errors.append("binary/artifact files forbidden in current tree: "+", ".join(bad[:20]))
for f in files:
    if re.search(r"(^|/)(node_modules|dist|out|\.next)/",f): errors.append(f"generated directory committed: {f}")
ap=argparse.ArgumentParser(); ap.add_argument("--site"); args=ap.parse_args()
if args.site:
    site=ROOT/args.site
    expected=["index.html","researchers/index.html","workspace/index.html","how-to/index.html","controls/index.html"]
    expected += [f"researchers/{r['slug']}/index.html" for r in rows]
    expected += [f"controls/{x}/index.html" for x in ("discussion","latex","presentation")]
    for rel in expected:
        if not (site/rel).is_file(): errors.append(f"site missing {rel}")
if errors:
    print("JP R&D VALIDATION: FAIL")
    for e in errors: print("- "+e)
    raise SystemExit(1)
print(f"JP R&D VALIDATION: PASS researchers={len(rows)} lanes={len(lane_names)} legacy={len(branches.get('archived_legacy',[]))}")
