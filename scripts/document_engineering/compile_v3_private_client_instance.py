#!/usr/bin/env python3
"""Compile a PRIVATE project instance of the SINGLE approved v3 client-contract layout.

This is not a second template. The caller supplies a private project-specific
master generated from the canonical v3 contract structure plus private overlays.
No source is published to CI and no PDF is approved by successful compilation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REG = ROOT / "registry/enterprise-document-types.json"
TYPE = "client-contract"

def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def check_canonical(source_root: Path):
    manifest=json.loads((source_root/"registry/enterprise-document-types.json").read_text(encoding="utf-8"))
    assert manifest["version"]=="3.0.0"
    items=[x for x in manifest["templates"] if x["id"]==TYPE]
    if len(items)!=1:
        raise ValueError("Exactly one canonical client-contract route is mandatory")
    contract=items[0]
    if contract["path"]!="templates/enterprise/v3/client-contract.tex":
        raise ValueError("Canonical contract template changed")
    path=source_root/contract["path"]
    style=source_root/"templates/enterprise/v3/enterprise-v3.sty"
    for file,sha in ((path,contract["approved_git_blob_sha"]),(style,manifest["style_git_blob_sha"])):
        if not file.is_file() or git_blob(file.read_bytes())!=sha:
            raise ValueError("Approved canonical v3 Git blob mismatch: "+str(file))
    return contract,manifest

def run(source_root:Path, project_root:Path, master:str):
    contract,registry=check_canonical(source_root)
    if "/" in master or "\\" in master or not master.endswith(".tex"):
        raise ValueError("Master must be an unqualified TeX filename")
    file=project_root/master
    if not file.is_file(): raise ValueError("Private project master not found")
    src=file.read_text(encoding="utf-8")
    if "\\usepackage{enterprise-v3}" not in src or "\\input{contract-content.tex}" not in src:
        raise ValueError("Private instance lacks canonical v3 stylesheet or project content input")
    if contract["approved_git_blob_sha"] not in src:
        raise ValueError("Private instance does not pin its approved canonical source Git blob")
    for key in ("contract-content.tex","company-brand.tex","enterprise-v3.sty"):
        if not (project_root/key).is_file():
            raise ValueError("Private source dependency missing: "+key)
    if git_blob((project_root/"enterprise-v3.sty").read_bytes())!=registry["style_git_blob_sha"]:
        raise ValueError("Private v3 style differs from approved release")
    if not shutil.which("latexmk"): raise RuntimeError("latexmk is required")
    p=subprocess.run(["latexmk","-pdf","-no-shell-escape","-interaction=nonstopmode",
                      "-halt-on-error",master],cwd=project_root,capture_output=True,text=True,timeout=180)
    if p.returncode:
        raise RuntimeError("LaTeX compilation failed:\n"+p.stdout[-1600:])
    pdf=project_root/(master[:-4]+".pdf")
    log=project_root/(master[:-4]+".log")
    if not pdf.is_file() or not log.is_file(): raise RuntimeError("Compiler did not return complete output")
    logs=log.read_text(encoding="utf-8",errors="replace")
    if "Overfull \\hbox" in logs or "Overfull \\vbox" in logs:
        raise RuntimeError("Text or graphics overflow; stop for visual QA")
    qa={"status":"DRAFT_RENDERED_PENDING_HUMAN_REVIEW",
        "source_control":"a9-enterprise-docs-v3.0.0",
        "canonical_type":TYPE,
        "canonical_blob":contract["approved_git_blob_sha"],
        "active_canonical_count":len([x for x in registry["templates"] if x["id"]==TYPE]),
        "project_tex_sha256":hashlib.sha256(src.encode()).hexdigest(),
        "output_pdf_sha256":hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "automatic_issuance":False}
    (project_root/(master[:-4]+".compile-qa.json")).write_text(json.dumps(qa,indent=2)+"\n")
    print(json.dumps(qa,indent=2))
    return qa

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repository",type=Path,default=ROOT)
    ap.add_argument("--project-dir",type=Path,required=True)
    ap.add_argument("--master",required=True)
    args=ap.parse_args()
    run(args.repository.resolve(),args.project_dir.resolve(),args.master)
