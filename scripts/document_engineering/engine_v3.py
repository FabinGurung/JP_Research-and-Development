#!/usr/bin/env python3
"""A9 Enterprise v3: one candidate LaTeX source per document type.

Compiles fictional review fixtures. Real private project data must be supplied
by an authorized executor, with authenticated evidence and human approval.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path
from resolve_template import resolve
from check_client_facing_language import violations, check_pdf, check_tex

ROOT=Path(__file__).resolve().parents[2]
REGISTRY=ROOT/"registry/enterprise-document-types.json"
TOKEN=re.compile(r"\{\{([a-z_]+)\}\}")
ESCAPE={"\\":r"\textbackslash{}","{":r"\{","}":r"\}","%":r"\%",
        "$":r"\$","&":r"\&","#":r"\#","_":r"\_","~":r"\textasciitilde{}",
        "^":r"\textasciicircum{}"}
DATE_KEYS={"issue_date","valid_until","effective_date","receipt_date",
           "payment_date","delivery_date","start_date","end_date"}
TABLE_FAMILIES={"vendor-quotation","government-quotation","estimate","material-report","purchase-order"}
SOURCE_GATES=("ORIGINAL_AUTHORITY","SEMANTIC_MAPPING","TYPED_DATA","COMPLETENESS",
              "COMPILATION","VISUAL_REVIEW","HUMAN_APPROVAL","PROVIDER_READBACK")

def escape(value):
    if not isinstance(value,str) or not value.strip() or len(value)>20000:
        raise ValueError("Required contractual fields must be nonempty text <= 20,000 chars")
    return "".join(ESCAPE.get(ch,ch) for ch in value).replace("\r\n","\n").replace("\n",r"\par "+"\n")

def inventory():
    reg=json.loads(REGISTRY.read_text(encoding="utf-8"))
    templates=reg["templates"]
    if len(templates)!=14 or len({t["id"] for t in templates})!=14:
        raise ValueError("One candidate per fourteen registered document types is mandatory")
    return {t["id"]:t for t in templates}

def table_render(rows):
    if not isinstance(rows,list) or not rows or len(rows)>50:
        raise ValueError("Table requires 1..50 sourced line records")
    body=[
        r"\par\smallskip",
        r"\noindent\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}X r l r@{}}",
        r"\toprule",
        r"\textbf{Illustrative description} & \textbf{Qty} & \textbf{Unit} & \textbf{Amount}\\",
        r"\midrule"
    ]
    for row in rows:
        if not isinstance(row,dict) or set(row)!={"description","quantity","unit","amount","source_ref"}:
            raise ValueError("Every item requires description, quantity, unit, amount and source ref")
        if not isinstance(row["source_ref"],str) or not row["source_ref"].strip():
            raise ValueError("Missing item provenance")
        body.append(" & ".join(escape(row[k]) for k in ("description","quantity","unit","amount"))+r"\\")
    body += [r"\bottomrule",r"\end{tabularx}",r"\par\smallskip"]
    return "\n".join(body)

def render(payload):
    if not isinstance(payload,dict):raise ValueError("JSON object required")
    typ=resolve(payload.get("template_id"))["id"]
    candidates=inventory()
    if typ not in candidates:raise ValueError("Unknown enterprise template type")
    info=candidates[typ]
    if payload.get("fixture_only") is not True and payload.get("source_context",{}).get("verified") is not True:
        raise ValueError("Non-fixture draft requires authenticated source context")
    fields=payload.get("fields")
    required=set(info["base_fields"])
    if not isinstance(fields,dict) or set(fields)!=required:
        raise ValueError("Missing, extra, or unknown field(s): "+str(sorted(required-set(fields or {})))+
                         " / "+str(sorted(set(fields or {})-required)))
    for k,v in fields.items():
        escape(v)
        if k in DATE_KEYS:
            try:date.fromisoformat(v)
            except ValueError as e:raise ValueError("ISO YYYY-MM-DD required: "+k) from e
    if "start_date" in fields and "end_date" in fields and fields["end_date"]<fields["start_date"]:
        raise ValueError("Period ends before start")
    source=(ROOT/info["path"]).read_text(encoding="utf-8")
    tokens=set(TOKEN.findall(source))
    computed={"document_status": ""}
    if typ in TABLE_FAMILIES:
        computed["document_table"]=table_render(payload.get("table_rows"))
        if payload.get("fixture_only") is not True:
            for row in payload["table_rows"]:
                if row["source_ref"].startswith("FICTIONAL-"):
                    raise ValueError("Fixture source refs forbidden in real project")
    elif payload.get("table_rows") is not None:
        raise ValueError("Unsupported table data on this document type")
    if tokens!=required|set(computed):
        raise ValueError("Typed schema and LaTeX template token mismatch: "+str(sorted(tokens^(required|set(computed)))))
    # The immutable v3 source is an internal layout authority, not its printed output.
    # Remove internal review/status furniture only from generated client copies.
    source=re.sub(r"(?m)^\\EnterpriseWarning\{DRAFT SAMPLE[^\n]*\}\s*$","",source)
    for tag in ("Reference","Organization ID"):
        source=re.sub(r"(?m)^\\EnterpriseMeta\{"+re.escape(tag)+r"\}\{[^\n]*\}\s*$","",source)
    source=source.replace(r"\\EnterpriseField{Project Identifier}",r"\\EnterpriseField{Project}")
    source=source.replace(r"\\EnterpriseField{CAD Quantity Ref}",r"\\EnterpriseField{Quantity source}")
    source=source.replace(r"\\EnterpriseField{Rate Library Ref}",r"\\EnterpriseField{Pricing basis}")
    source=source.replace(r"\\EnterpriseField{BOQ Template Ref}",r"\\EnterpriseField{Schedule of quantities}")
    # Freeze output presentation, not the canonical .sty or original template source.
    output_headers=(r"\\fancyhead[L]{}\\fancyhead[R]{}\\fancyfoot[L]{}")
    source=source.replace(r"\\begin{document}",r"\\begin{document}"+"\n"+output_headers,1)
    visible_keys=set(TOKEN.findall(source)) - {"document_status"}
    for k in sorted(visible_keys):
        issues=violations(fields[k])
        if issues:raise ValueError("Client-visible field "+k+" violates language policy: "+", ".join(issues))
    result=TOKEN.sub(lambda m:computed[m.group(1)] if m.group(1) in computed else escape(fields[m.group(1)]),source)
    if TOKEN.search(result):raise ValueError("Unresolved placeholder")
    if violations(result):
        raise ValueError("Client-facing LaTeX contains prohibited identifiers/status: "+", ".join(violations(result)))
    qa={"type_id":typ,"state":"FICTIONAL_QA_SAMPLE" if payload.get("fixture_only") else "DRAFT_NOT_SIGNABLE",
        "originals_unchanged":True,"template_path":info["path"],
        "source_sha256":hashlib.sha256(source.encode()).hexdigest(),
        "rendered_tex_sha256":hashlib.sha256(result.encode()).hexdigest(),
        "release_gates":{k:"HOLD_UNLESS_SEPARATELY_VERIFIED" for k in SOURCE_GATES},
        "auto_approve":False,"fixture_only":payload.get("fixture_only") is True}
    return result,qa

def build(payload,out,compile_pdf=False):
    tex,qa=render(payload)
    out.mkdir(parents=True,exist_ok=True)
    name=qa["type_id"]
    target=out/(name+".tex")
    target.write_text(tex,encoding="utf-8")
    check_tex(target)
    shutil.copy2(ROOT/"templates/enterprise/v3/enterprise-v3.sty",out/"enterprise-v3.sty")
    if compile_pdf:
        if not shutil.which("latexmk"):raise RuntimeError("No latexmk compiler")
        process=subprocess.run(
            ["latexmk","-pdf","-no-shell-escape","-interaction=nonstopmode",
             "-halt-on-error",name+".tex"],
            cwd=out,capture_output=True,text=True,timeout=180)
        if process.returncode or not target.with_suffix(".pdf").is_file():
            raise RuntimeError("PDF compile failed: "+name+"\n"+process.stdout[-2600:])
        logfile=target.with_suffix(".log").read_text(errors="replace")
        if "Overfull \\hbox" in logfile or "Overfull \\vbox" in logfile:
            raise ValueError("Unresolved page margin overflow: "+name)
        pdf=target.with_suffix(".pdf")
        check_pdf(pdf)
        qa["pdf_client_language"]="PASS"
        qa["pdf_sha256"]=hashlib.sha256(pdf.read_bytes()).hexdigest()
        qa["pdf_size_bytes"]=pdf.stat().st_size
        qa["compilation"]="PASS_TECHNICAL_VISUAL_REVIEW_PENDING"
    else:qa["compilation"]="SOURCE_ONLY"
    (out/(name+".qa.json")).write_text(json.dumps(qa,indent=2)+"\n",encoding="utf-8")
    return qa

def selftest():
    candidates=inventory()
    count=0
    for typ in sorted(candidates):
        file=ROOT/"examples/document-engineering/v3"/(typ+".sample.json")
        data=json.loads(file.read_text())
        tex,qa=render(data)
        assert qa["state"]=="FICTIONAL_QA_SAMPLE"
        assert r"\EnterpriseHeading" in tex
        assert "{{" not in tex
        fail=json.loads(json.dumps(data))
        fail["fields"].pop("document_ref")
        try:render(fail)
        except ValueError:pass
        else:raise AssertionError("Missing required field accepted")
        count+=1
    # A database-style client name must be rejected rather than silently rewritten.
    negative=json.loads((ROOT/"examples/document-engineering/v3/client-contract.sample.json").read_text())
    negative["fields"]["project_identifier"]="07_Example_Client"
    try:render(negative)
    except ValueError:pass
    else:raise AssertionError("Machine-like project name reached printable output")
    print(f"PASS {count}/14 typed templates and client-visible semantics")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data",type=Path);p.add_argument("--out",type=Path)
    p.add_argument("--compile",action="store_true")
    p.add_argument("--demo-all",action="store_true")
    p.add_argument("--self-test",action="store_true")
    args=p.parse_args()
    if args.self_test:selftest();return
    if not args.out:p.error("--out is required")
    if args.demo_all:
        for typ in sorted(inventory()):
            payload=json.loads((ROOT/"examples/document-engineering/v3"/(typ+".sample.json")).read_text())
            result=build(payload,args.out/typ,args.compile)
            print(typ,result["compilation"])
    elif args.data:
        print(json.dumps(build(json.loads(args.data.read_text(encoding="utf-8")),args.out,args.compile),indent=2))
    else:p.error("Use --data or --demo-all")
if __name__=="__main__":main()
