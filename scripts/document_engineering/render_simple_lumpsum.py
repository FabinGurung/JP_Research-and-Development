#!/usr/bin/env python3
"""A9 private-input, public-source renderer for simple lump-sum client agreements."""
import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from check_client_facing_language import violations, check_pdf

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/"templates/enterprise/v2/client-contract-simple-lumpsum.tex"
STYLE=ROOT/"templates/enterprise/v2/enterprise-shared.sty"
NUMBER_NAMES=("Zero","One","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten",
              "Eleven","Twelve","Thirteen","Fourteen","Fifteen","Sixteen","Seventeen","Eighteen","Nineteen")
TENS={2:"Twenty",3:"Thirty",4:"Forty",5:"Fifty",6:"Sixty",7:"Seventy",8:"Eighty",9:"Ninety"}
ESC={"\\":r"\textbackslash{}","&":r"\&","%":r"\%","$":r"\$","#":r"\#",
     "_":r"\_","{":r"\{","}":r"\}","~":r"\textasciitilde{}"}
TOKEN=re.compile(r"@@[A-Z_]+@@")

def escape(s):
    if not isinstance(s,str): raise ValueError("Text expected")
    return "".join(ESC.get(c,c) for c in s)

def small(n):
    if n<20:return NUMBER_NAMES[n]
    if n<100:return TENS[n//10]+("-"+NUMBER_NAMES[n%10] if n%10 else "")
    return NUMBER_NAMES[n//100]+" Hundred"+(" "+small(n%100) if n%100 else "")

def price_words(n):
    if not (0<n<1000000000):raise ValueError("Unsupported contract amount")
    parts=[]
    for label,size in [("Crore",10000000),("Lakh",100000),("Thousand",1000)]:
        if n>=size:
            x,n=divmod(n,size)
            parts.append(small(x)+" "+label)
    if n:parts.append(small(n))
    return "Rupees "+" ".join(parts)+" Only"

def npr_commas(n):
    s=str(n)
    if len(s)<=3:return s
    first,last=s[:-3],s[-3:]
    chunks=[]
    while len(first)>2:chunks.insert(0,first[-2:]);first=first[:-2]
    if first:chunks.insert(0,first)
    return ",".join(chunks+[last])

def render(data):
    if data.get("template_id")!="client-contract-simple-lumpsum":raise ValueError("Wrong template_id")
    required=("company_name","owner_name","project_name","demolition_clause",
              "materials_clause","completion_clause","confirmation_clause")
    if any(not isinstance(data.get(k),str) or not data[k].strip() for k in required):
        raise ValueError("Missing contractual text")
    n,area=data.get("total_npr"),data.get("house_area_sqft")
    if type(n) is not int or n<=0 or type(area) is not int or area<=0:
        raise ValueError("Amount and area must be positive whole numbers")
    scope=data.get("scope_items")
    if not isinstance(scope,list) or not scope or any(
        not isinstance(item,dict) or not isinstance(item.get("heading"),str) or
        not item["heading"].strip() or not isinstance(item.get("description"),str)
        for item in scope):
        raise ValueError("Missing scope items")
    plain="\n".join([*(data[k] for k in required),
                     *(item["heading"]+" "+item["description"] for item in scope)])
    problems=violations(plain)
    if problems:raise ValueError("Internal terms forbidden in client copy: "+", ".join(problems))
    fields={
        "@@CONTRACTOR_UPPER@@":escape(data["company_name"].upper()),
        "@@CONTRACTOR_NAME@@":escape(data["company_name"]),
        "@@CLIENT_NAME@@":escape(data["owner_name"]),
        "@@PROJECT_NAME@@":escape(data["project_name"]),
        "@@HOUSE_AREA@@":npr_commas(area)+" square feet",
        "@@PRICE_NPR@@":npr_commas(n),
        "@@PRICE_WORDS@@":price_words(n),
        "@@SITE_ADDRESS@@":escape(data["site_address"]) if data.get("site_address") else r"\underline{\hspace{95mm}}",
        "@@AGREEMENT_DATE@@":escape(data["agreement_date"]) if data.get("agreement_date") else r"\underline{\hspace{48mm}}",
        "@@SCOPE_ITEMS@@":"\n".join(r"\item \textbf{"+escape(i["heading"])+"} "+escape(i["description"]) for i in scope),
        "@@DEMOLITION_CLAUSE@@":escape(data["demolition_clause"]),
        "@@MATERIAL_CLAUSE@@":escape(data["materials_clause"]),
        "@@COMPLETION_CLAUSE@@":escape(data["completion_clause"]),
        "@@CONFIRMATION_CLAUSE@@":escape(data["confirmation_clause"]),
        "@@CONTRACTOR_SIGNATORY@@":escape(data.get("contractor_signatory") or "Authorized representative")
    }
    text=SOURCE.read_text(encoding="utf-8")
    if set(TOKEN.findall(text))!=set(fields):raise ValueError("Template field mismatch")
    for k,v in fields.items():text=text.replace(k,v)
    if TOKEN.search(text):raise ValueError("Unresolved source token")
    return text

def produce(data,out,compile_pdf=False):
    out.mkdir(parents=True,exist_ok=True)
    tex=out/"construction-works-agreement.tex"
    tex.write_text(render(data),encoding="utf-8")
    shutil.copy2(STYLE,out/"enterprise-shared.sty")
    report={"state":"DRAFT_ONLY","source_type":"client-contract-simple-lumpsum",
            "amount_npr":data["total_npr"],"area_sqft":data["house_area_sqft"],
            "scope_item_count":len(data["scope_items"]),"legal_approval":False,
            "signable":False,"taxes_payment_dates_and_specs":"REQUIRES_REVIEW"}
    if compile_pdf:
        if not shutil.which("latexmk"):raise RuntimeError("LaTeX renderer unavailable")
        r=subprocess.run(["latexmk","-pdf","-no-shell-escape","-halt-on-error",
                          "-interaction=nonstopmode",tex.name],
                         cwd=out,capture_output=True,text=True,timeout=150)
        if r.returncode:raise RuntimeError("LaTeX compilation failed "+r.stdout[-1300:])
        check_pdf(tex.with_suffix(".pdf"))
        report["pdf_technical_check"]="PASS_TEXT_SCAN_VISUAL_REVIEW_STILL_REQUIRED"
    (out/"draft-qa.json").write_text(json.dumps(report,indent=2)+"\n")
    return report

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--data",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--compile",action="store_true")
    args=p.parse_args()
    print(json.dumps(produce(json.loads(args.data.read_text()),args.out,args.compile),indent=2))
