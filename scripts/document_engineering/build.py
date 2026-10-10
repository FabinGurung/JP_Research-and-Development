#!/usr/bin/env python3
"""Public-safe LaTeX code. Process private data only on an authorized local runner."""
import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = {
    "works-contract": ("works_contract.tex", ("contract_ref", "organization", "client", "contractor", "project", "location", "effective_date", "scope", "measurement_and_rates", "schedule", "payment_terms", "quality_terms", "variation_terms")),
    "experience-letter": ("experience_letter.tex", ("organization", "issue_date", "employee", "role", "start_date", "end_date", "duties", "signatory")),
    "salary-contract": ("salary_contract.tex", ("organization", "employee", "position", "start_date", "salary", "pay_cycle", "duties", "terms"))
}
SPECIAL = {
    "\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "%": r"\%",
    "$": r"\$", "&": r"\&", "#": r"\#", "_": r"\_",
    "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"
}
TOKEN = re.compile(r"\{\{([a-z_]+)\}\}")

def escape_tex(value):
    if not isinstance(value, str) or not value.strip() or len(value)>15000:
        raise ValueError("Every required field must be a nonempty JSON string (max 15,000 characters)")
    return "".join(SPECIAL.get(c,c) for c in value).replace("\r\n","\n").replace("\n","\n\n")

def render(data):
    if not isinstance(data,dict) or data.get("template_id") not in TEMPLATES:
        raise ValueError("Unknown template_id")
    filename, required = TEMPLATES[data["template_id"]]
    fields = data.get("fields")
    if not isinstance(fields,dict) or set(fields)!=set(required):
        raise ValueError("Input fields do not match the template schema")
    template = (ROOT/"templates"/"enterprise"/filename).read_text(encoding="utf-8")
    if set(TOKEN.findall(template))!=set(required):
        raise ValueError("Template placeholder/schema mismatch")
    result = TOKEN.sub(lambda m: escape_tex(fields[m.group(1)]),template)
    if TOKEN.search(result):
        raise ValueError("Unresolved token")
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--compile",action="store_true")
    a=p.parse_args()
    payload=json.loads(a.data.read_text(encoding="utf-8"))
    latex=render(payload)
    a.out.mkdir(parents=True,exist_ok=True)
    dest=a.out/(payload["template_id"]+".tex")
    dest.write_text(latex,encoding="utf-8")
    print("Private/local TeX output:",dest)
    if a.compile:
        if not shutil.which("latexmk"):
            raise SystemExit("Install latexmk/TeX Live before --compile")
        subprocess.run(["latexmk","-pdf","-no-shell-escape","-halt-on-error","-interaction=nonstopmode",dest.name],cwd=a.out,check=True,timeout=120)
        print("Local PDF:",dest.with_suffix(".pdf"))

if __name__=="__main__":
    main()
