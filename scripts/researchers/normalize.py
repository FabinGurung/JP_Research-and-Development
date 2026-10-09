#!/usr/bin/env python3
"""Read-only R&D researcher Drive-role planner, registry validator and handover generator.

Never calls Google Drive, mutates folders, or acknowledges A9 Main. Registry was
provider-read at a point in time and must be refreshed by each owning researcher.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
REG=ROOT/"registry/researcher-folder-roles.json"
RESEARCHERS=ROOT/"registry/researchers.json"
ALLOWED={"VERIFIED_DIRECT_CHILD","VERIFIED_ID_ALIAS_REVIEW","NOT_OBSERVED_DIRECT_CHILD","HOLD_ROOT_UNVERIFIED"}
PREFIX="https://drive.google.com/drive/folders/"

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def validate(reg=None, people=None):
    reg=reg or load(REG)
    people=people or load(RESEARCHERS)["researchers"]
    errors=[]
    expected={(x["researcher_id"],x["slug"]):x for x in people}
    records=reg.get("records",[])
    canonical=reg.get("canonical_roles",[])
    if len(records)!=len(expected) or len(set(canonical))!=len(canonical):
        errors.append("incorrect researcher count or duplicate logical roles")
    identities=set()
    roots=set()
    for p in records:
        key=(p.get("researcher_id"),p.get("researcher_slug"))
        if key not in expected or key in identities:
            errors.append("unregistered or duplicate researcher "+str(key))
            continue
        identities.add(key)
        registered_root=expected[key].get("drive",{}).get("project_root_drive_id")
        actual_root=p.get("existing_project_root_drive_id")
        if registered_root!=actual_root:
            errors.append("project root differs from researcher registry "+str(key))
        if actual_root:
            if actual_root in roots: errors.append("duplicate researcher root "+actual_root)
            roots.add(actual_root)
        elif p.get("root_status")!="HOLD_NO_VERIFIED_ROOT":
            errors.append("missing root not marked HOLD "+str(key))
        if p.get("project_id") is not None and not p.get("project_id_evidence"):
            errors.append("project_id without authenticated A9 proof "+str(key))
        rows=p.get("roles",[])
        if {x.get("logical_role") for x in rows}!=set(canonical) or len(rows)!=len(canonical):
            errors.append("missing or duplicate canonical roles "+str(key))
        for item in rows+p.get("researcher_specific_extensions",[]):
            folder=item.get("existing_drive_folder_id")
            if folder:
                if not item.get("current_name") or item.get("action") not in ("REUSE_EXISTING_ID","PRESERVE"):
                    errors.append("invalid grounded folder role "+str(key))
            elif item.get("current_name"):
                errors.append("imaginary folder name without Drive ID "+str(key))
            if item.get("physical_mutation_performed") is not False:
                errors.append("central scope may never claim physical mutation "+str(key))
            if item in rows and item.get("status") not in ALLOWED:
                errors.append("unknown role state "+str(item.get("status")))
            if item.get("approved_alias") and item.get("approved_alias")!=item.get("current_name"):
                errors.append("unapproved changed alias "+str(key))
    if identities!=set(expected):
        errors.append("researcher registry identity mismatch")
    if len(roots)!=10 or reg.get("verified_root_count")!=10:
        errors.append("verified root count is not 10")
    if reg.get("writes_to_drive")!=0:
        errors.append("read-only migration unexpectedly has Drive writes")
    return errors

def plan(person):
    available=[x for x in person["roles"] if x["existing_drive_folder_id"]]
    gaps=[x for x in person["roles"] if not x["existing_drive_folder_id"]]
    alias=[x for x in available if x["status"]=="VERIFIED_ID_ALIAS_REVIEW"]
    return {
        "researcher_id":person["researcher_id"],
        "slug":person["researcher_slug"],
        "project_id":person["project_id"],
        "project_root_id":person["existing_project_root_drive_id"],
        "action":"NO_CENTRAL_MUTATIONS",
        "reuse":available,
        "unobserved_or_hold":gaps,
        "alias_review":alias,
        "preserved_specializations":person["researcher_specific_extensions"],
        "governed_next":"Owner thread performs fresh root/child readback, records PRE, only authorized physical mutations, POST and Local registration; never auto-ACK Main.",
        "root_gate":person["root_status"]
    }

def handover(person):
    p=plan(person)
    lines=[
        "# "+person["researcher_id"]+" — "+person["researcher_slug"]+" folder handover",
        "",
        "**Status:** READ-ONLY DRIVE-ID ROLE MAPPING; NOT A PHYSICAL MIGRATION OR SCIENTIFIC APPROVAL.",
        "**Upstream:** R&D single folder contract; current owning project/A9 controls overrule stale discovery.",
        "",
        "Project ID: "+str(person["project_id"] or "HOLD — no canonical A9 project_id verified"),
        "Project root: "+(PREFIX+p["project_root_id"] if p["project_root_id"] else "HOLD — no verified root; DO NOT CREATE"),
        "",
        "## Verified existing folders — REUSE existing IDs",
        ""
    ]
    for x in p["reuse"]:
        lines.append("- "+x["logical_role"]+": "+x["current_name"]+" — "+PREFIX+x["existing_drive_folder_id"]+" ("+x["status"]+")")
    lines+=["","## Not verified as direct children — do not auto-create",""]
    lines.extend("- "+x["logical_role"]+" — "+x["status"] for x in p["unobserved_or_hold"])
    lines+=["","## Specialized folders — preserve",""]
    lines.extend("- "+x["logical_role"]+": "+x["current_name"]+" — "+PREFIX+x["existing_drive_folder_id"] for x in p["preserved_specializations"])
    lines+=["","## Physical migration execution gate","",
            "1. Fresh-read live owning project root, current A9 Local/Main and project scientific/source controls.",
            "2. Compare this discovery mapping to actual current child IDs, names, permissions and dependencies.",
            "3. Mark REUSE for matching roles; propose new folders/renames only if necessary and explicitly approved.",
            "4. PRE snapshot via approved A9 procedure and record exact IDs and reverse links.",
            "5. Make only bounded, user-authorized Drive mutations; never delete, mass-move or silently overwrite.",
            "6. Provider-read POST, update A9 ArtifactRegistry/ArtifactEdges/VersionLog/RunLog and checkpoint.",
            "7. Main Library sync requires separate owning A9 approval/ACK; scientific manuscript is out of scope.",
            "",
            "**Remaining:** aliases and unobserved child roles require researcher-side review; no changes made in this package.",
            ""]
    return "\n".join(lines)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--validate",action="store_true")
    ap.add_argument("--researcher",help="RSH-xxx ID or researcher slug; default all")
    ap.add_argument("--json",action="store_true")
    ap.add_argument("--emit-handovers",type=Path,help="Write LOCAL generated handover text, never Drive")
    args=ap.parse_args()
    reg=load(REG)
    problems=validate(reg)
    if problems:
        print("FOLDER ROLES VALIDATION FAIL:\n"+"\n".join(problems))
        raise SystemExit(1)
    if args.validate: print("FOLDER ROLES VALIDATION PASS researchers=11 roots=10")
    entries=reg["records"]
    if args.researcher:
        entries=[x for x in entries if args.researcher in (x["researcher_id"],x["researcher_slug"])]
        if not entries: ap.error("researcher not registered")
    if args.json: print(json.dumps([plan(x) for x in entries],indent=2))
    elif not args.validate:
        for x in entries:
            p=plan(x)
            print(f'{p["researcher_id"]} root={p["root_gate"]} reuse={len(p["reuse"])} alias_review={len(p["alias_review"])} missing={len(p["unobserved_or_hold"])}')
    if args.emit_handovers:
        args.emit_handovers.mkdir(parents=True,exist_ok=True)
        for x in entries:
            path=args.emit_handovers/(x["researcher_id"]+"__folder_handover.md")
            path.write_text(handover(x),encoding="utf-8")
        print("LOCAL HANDOVERS WRITTEN "+str(args.emit_handovers))

if __name__=="__main__":
    main()
