#!/usr/bin/env python3
"""Fail-closed lint for ONE canonical R&D thesis LaTeX tower; no source/PDF compile."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
errors=[]

def doc(rel):
    p=ROOT/rel
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError,ValueError) as e:
        errors.append(f"missing/invalid {rel}: {e}")
        return {}

tower=doc("controls/latex/tower.json")
core=doc("controls/latex/core-rules.json")
inherit=doc("registry/latex-inheritance.json")
changelog=doc("controls/latex/change-register.json")
extensions=doc("controls/latex/extension-registry.json")
alias=doc("controls/latex.control.json")
registry=doc("registry/researchers.json")
canonical="controls/latex/tower.json"
sty="controls/latex/template/pumlsc-shared.sty"

if tower.get("control_id")!="RD-CONTROL-LATEX-001" or tower.get("authority_path")!=canonical:
    errors.append("no single canonical authority")
if tower.get("template_entry")!=sty or not (ROOT/sty).is_file():
    errors.append("missing canonical shared .sty template")
if alias.get("status")!="ALIAS_ROUTING_ONLY_NOT_SECOND_TOWER" or alias.get("source_code")!=canonical:
    errors.append("legacy alias still claims independent tower")
if alias.get("production_rules") or alias.get("project_overrides"):
    errors.append("legacy alias duplicates operational policy")
if tower.get("a7_role")!="ID_ROUTING_ONLY__NEVER_OWNS_LATEX_TOWER":
    errors.append("A7 must remain out of LaTeX ownership")
core_entries=core.get("rules",[])
coreids=[x.get("id") for x in core_entries]
if len(coreids)!=len(set(coreids)) or not coreids:
    errors.append("missing or duplicate core rules")
for k in coreids:
    try: n=int(re.fullmatch(r"RD-LTX-CORE-(\d{3})",k).group(1))
    except (AttributeError,TypeError,ValueError): errors.append("invalid core ID "+str(k));continue
    if not 1<=n<=100: errors.append("shared rule reserved range exceeded: "+k)

researcher_rows=registry.get("researchers",[])
inherit_rows=inherit.get("researchers",[])
expected={(r.get("researcher_id"),r.get("slug")) for r in researcher_rows}
actual=[(r.get("researcher_id"),r.get("slug")) for r in inherit_rows]
if len(actual)!=len(expected) or set(actual)!=expected:
    errors.append("EVERY registered researcher must inherit SAME template, no omissions/duplicates")
for r in inherit_rows:
    if r.get("tower")!=canonical or r.get("template")!=sty or r.get("no_local_base_copy") is not True:
        errors.append("researcher deviates from shared tower: "+str(r.get("slug")))
    c=r.get("local_configuration")
    if c:
        config=doc(c)
        if config.get("researcher_id")!=r.get("researcher_id") or config.get("shared_control")!=canonical or config.get("shared_template")!=sty:
            errors.append("project configuration is not inherited-only: "+c)

recorded=changelog.get("entries",[])
change_numbers=[]
for c in recorded:
    identifier=c.get("change_id")
    try: num=int(re.fullmatch(r"RD-LTX-CHG-(\d+)",identifier).group(1))
    except (AttributeError,ValueError,TypeError): errors.append("invalid central change ID "+str(identifier));continue
    if num<101: errors.append("central amendments start at 101")
    change_numbers.append(num)
    if c.get("researcher_id") not in {x[0] for x in expected}:
        errors.append("unregistered change researcher")
    if c.get("classification") not in ("GLOBAL_CANDIDATE","RESEARCHER_ONLY"):
        errors.append("change classification required")
    if not c.get("summary") or not c.get("before_after_qa_evidence"):
        errors.append("change must carry reason and proof reference")
if len(set(change_numbers))!=len(change_numbers): errors.append("duplicate amendment number")
if changelog.get("next_number")!=(max(change_numbers,default=100)+1):
    errors.append("change counter not append-only")

recorded_extension_paths=set()
for x in extensions.get("registered",[]):
    p=x.get("path","")
    slug=x.get("researcher_slug","")
    if not p.startswith(f"researchers/{slug}/latex/extensions/"):
        errors.append("extension outside scoped researcher folder: "+p)
    if not any(r.get("slug")==slug for r in researcher_rows):
        errors.append("extension researcher not registered")
    if x.get("change_id") not in {c.get("change_id") for c in recorded}:
        errors.append("extension without central numbered amendment "+p)
    recorded_extension_paths.add(p)
    if not (ROOT/p).is_file():
        errors.append("registered researcher extension path not found: "+p)

# Every adopted researcher source must import shared .sty and may not check in any copy.
for p in (ROOT/"researchers").glob("*/latex/**/*"):
    if not p.is_file(): continue
    relative=p.relative_to(ROOT).as_posix()
    if p.name=="pumlsc-shared.sty" or "/template/" in relative:
        errors.append("DUPLICATE CENTRAL TEMPLATE forbidden: "+relative)
    if p.suffix.lower() in {".sty",".cls"} and relative not in recorded_extension_paths:
        errors.append("unregistered researcher styling code: "+relative)
    if p.name=="main.tex":
        content=p.read_text(encoding="utf-8")
        if r"\usepackage{pumlsc-shared}" not in content:
            errors.append("admitted manuscript missing central style import: "+relative)
for p in (ROOT/"researchers").glob("*/latex/extensions/**/*"):
    if p.is_file() and p.relative_to(ROOT).as_posix() not in recorded_extension_paths:
        errors.append("unregistered researcher extension source: "+p.relative_to(ROOT).as_posix())

# Safal-derived cross-researcher semantic inheritance requires one canonical owner.
semantic_path="controls/latex/authorial-voice-policy.json"
checker_path="scripts/latex/check_authorial_voice.py"
semantic=doc(semantic_path)
if semantic.get("canonical_owner")!=canonical: errors.append("competing semantic tower")
if tower.get("rules",{}).get("semantic")!=semantic_path: errors.append("semantic tower pointer absent")
if tower.get("rules",{}).get("validation")!=checker_path: errors.append("semantic checker pointer absent")
if not (ROOT/checker_path).is_file(): errors.append("missing shared semantic checker")
for row in inherit_rows:
    if row.get("semantic_policy")!=semantic_path or row.get("semantic_checker")!=checker_path:
        errors.append("missing researcher semantic inheritance: "+str(row.get("slug")))

# Shared code should not include private binaries; this validator makes no compile claim.
txt=(ROOT/sty).read_text(encoding="utf-8") if (ROOT/sty).is_file() else ""
for test in [r"\setmainfont{Times New Roman}",r"\onehalfspacing","left=3cm",r"\newcommand{\PUStartMainBody}"]:
    if test not in txt: errors.append("shared style baseline missing: "+test)
if errors:
    print("SINGLE LATEX INHERITANCE: FAIL")
    for problem in errors: print("- "+problem)
    sys.exit(1)
print(f"SINGLE LATEX INHERITANCE: PASS canonical=1 researchers={len(actual)} shared_rules={len(coreids)} amendments={len(recorded)} scoped_extensions={len(recorded_extension_paths)} (SOURCE-ONLY)")
