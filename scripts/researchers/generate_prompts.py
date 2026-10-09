#!/usr/bin/env python3
"""Reproducibly generate/check researcher-scoped opt-in prompts from one template."""
from __future__ import annotations
import argparse,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"scripts/researchers"))
from normalize import load,validate
def render(row,name,template):
    root=row["existing_project_root_drive_id"]
    roles="\n".join(
        "- "+x["logical_role"]+": "+(x["current_name"]+" | Drive "+x["existing_drive_folder_id"]+" | https://drive.google.com/drive/folders/"+x["existing_drive_folder_id"]+" | "+x["status"]
        if x["existing_drive_folder_id"] else "NOT VERIFIED at root; do not autocreate")
        for x in row["roles"])
    specials="\n".join("- "+x["logical_role"]+": "+x["current_name"]+" | Drive "+x["existing_drive_folder_id"]+" | https://drive.google.com/drive/folders/"+x["existing_drive_folder_id"] for x in row["researcher_specific_extensions"]) or "None recorded; preserve other live specializations."
    gaps=", ".join(x["logical_role"] for x in row["roles"] if x["existing_drive_folder_id"] is None) or "None observed."
    values={"ID":row["researcher_id"],"NAME":name,"SLUG":row["researcher_slug"],"ROOT":root or "HOLD — UNVERIFIED","ROOT_LINK":"https://drive.google.com/drive/folders/"+root if root else "HOLD — NO VERIFIED ROOT","ROLES":roles,"SPECIAL":specials,"GAPS":gaps,
       "ROOT_NOTE":"CRITICAL ROOT HOLD: No verified project root for this researcher. DO NOT physically reorganize any location until owning A9 identifies an exact project and approves its root." if not root else "Root ID was verified in the earlier read-only Drive audit; read the provider afresh before all mutations."}
    for key,value in values.items():
        template=template.replace("@@"+key+"@@",value)
    if "@@" in template: raise ValueError("Unresolved token for "+row["researcher_id"])
    return template
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--check",action="store_true")
    ap.add_argument("--researcher",default=None)
    args=ap.parse_args()
    registry=load(ROOT/"registry/researcher-folder-roles.json")
    ppl=load(ROOT/"registry/researchers.json")["researchers"]
    problems=validate(registry,ppl)
    if problems:raise SystemExit("Source folder registry INVALID: "+"; ".join(problems))
    names={x["researcher_id"]:x["display_name"] for x in ppl}
    template=(ROOT/"prompts/researcher_owner_execution_master.md").read_text(encoding="utf-8")
    count=0
    for row in registry["records"]:
        if args.researcher and args.researcher not in (row["researcher_id"],row["researcher_slug"]):continue
        name=row["researcher_id"]+"__"+row["researcher_slug"]+".md"
        file=ROOT/"prompts/researchers"/name
        expected=render(row,names[row["researcher_id"]],template)
        if args.check:
            if not file.is_file() or file.read_text(encoding="utf-8")!=expected:
                problems.append("Mismatch or missing handover "+name)
        else:
            file.parent.mkdir(parents=True,exist_ok=True)
            file.write_text(expected,encoding="utf-8")
            print("GENERATED "+name)
        count+=1
    if count==0 or problems:
        raise SystemExit("OWNER HANDOVER FAIL "+str(problems or ["No researcher selected"]))
    print("OWNER HANDOVER PASS "+str(count))
if __name__=="__main__":
    main()
