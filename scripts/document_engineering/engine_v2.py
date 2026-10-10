#!/usr/bin/env python3
"""DRAFT-only enterprise template renderer. Private inputs stay outside Git."""
import json
import re
import argparse
import datetime
import shutil
import tempfile
from pathlib import Path
from validation_v2 import validate
from check_client_facing_language import violations
ROOT=Path(__file__).resolve().parents[2]
TOKEN=re.compile(r"\{\{([a-z_]+)\}\}")
ESC={"&":r"\&","%":r"\%","$":r"\$","#":r"\#","_":r"\_","{":r"\{","}":r"\}","\\":r"\textbackslash{}"}
def escape(value):
    if not isinstance(value,str) or not value.strip() or len(value)>20000: raise ValueError("Missing or overlong text")
    return "".join(ESC.get(c,c) for c in value)
def render(document):
    kind=document["template_id"]
    if not re.fullmatch("[a-z-]+",kind):raise ValueError("Invalid document type")
    config=json.loads((ROOT/"controls/document-engineering/types"/(kind+".json")).read_text())
    fields=document["fields"]
    if not isinstance(fields,dict) or set(fields)!=set(config["required_fields"]): raise ValueError("Required fields mismatch")
    for k,v in fields.items():
        escape(v)
        if k=="issue_date" or k.endswith("_date"):
            try: datetime.date.fromisoformat(v)
            except ValueError: raise ValueError("Date must be YYYY-MM-DD: "+k) from None
    if "start_date" in fields and "end_date" in fields and fields["start_date"]>fields["end_date"]:
        raise ValueError("End date before start date")
    disallowed=violations('\n'.join(fields.values()))
    if disallowed:raise ValueError('Client document contains forbidden internal terminology: '+', '.join(disallowed))
    arithmetic=validate(document)
    source=(ROOT/"templates/enterprise/v2"/(kind+".tex")).read_text()
    if set(TOKEN.findall(source))!=set(fields): raise ValueError("Template/schema mismatch")
    output=TOKEN.sub(lambda match:escape(fields[match.group(1)]),source)
    gates={g:"HOLD_REQUIRES_INDEPENDENT_EVIDENCE" for g in config["approval_gates"]}
    return output,{"state":"DRAFT_NOT_SIGNABLE","release":"BLOCKED_HUMAN_REVIEW",
                   "type_id":kind,"arithmetic":arithmetic,"gates":gates,"auto_sign":False}

def demo(kind):
    spec=json.loads((ROOT/"controls/document-engineering/types"/(kind+".json")).read_text())
    fields={}
    for f in spec["required_fields"]:
        if f=="issue_date" or f.endswith("_date"): fields[f]="2026-10-10"
        elif f=="document_ref":fields[f]="DEMO-001"
        elif f=="organization_id":fields[f]="DEMO-ORG-001"
        else:fields[f]="Fictional sample only"
    return {"template_id":kind,"fields":fields}

def write_draft(document,out):
    out.mkdir(parents=True,exist_ok=True)
    tex,qa=render(document)
    kind=document["template_id"]
    (out/(kind+".tex")).write_text(tex,encoding="utf-8")
    shutil.copy2(ROOT/"templates/enterprise/v2/enterprise-shared.sty",out/"enterprise-shared.sty")
    (out/(kind+".qa.json")).write_text(json.dumps(qa,indent=2)+"\n",encoding="utf-8")

def selftest():
    paths=list((ROOT/"controls/document-engineering/types").glob("*.json"))
    assert len(paths)==14
    with tempfile.TemporaryDirectory() as scratch:
        for f in paths:
            p=demo(f.stem)
            write_draft(p,Path(scratch)/f.stem)
            try:render({"template_id":f.stem,"fields":{}})
            except ValueError:pass
            else:raise AssertionError("Missing required fields accepted")
        bad=demo("estimate")
        bad["financials"]={"items":[{"description":"Sample","unit":"m2","source_ref":"DEMO",
            "quantity":2,"rate":3,"amount":5}],"tax":0,"subtotal":5,"grand_total":5}
        try:render(bad)
        except ValueError:pass
        else:raise AssertionError("Arithmetic mismatch accepted")
    print("PASS 14/14 typed draft sources, schema holds, arithmetic rejection")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data",type=Path);ap.add_argument("--out",type=Path)
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--demo-all",action="store_true")
    a=ap.parse_args()
    if a.self_test:selftest();return
    if not a.out:ap.error("--out required")
    if a.demo_all:
        for f in sorted((ROOT/"controls/document-engineering/types").glob("*.json")):
            write_draft(demo(f.stem),a.out/f.stem)
    elif a.data:write_draft(json.loads(a.data.read_text(encoding="utf-8")),a.out)
    else:ap.error("--data or --demo-all required")
if __name__=="__main__":main()
