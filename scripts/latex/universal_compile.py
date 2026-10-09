#!/usr/bin/env python3
"""Universal explicit thesis XeLaTeX/Biber runner. Never runs automatically.

Requires verified *owning* project source admission JSON and explicit --execute.
The emitted PDF is at most a technical review candidate; full university-format,
human visual, scientific approval, Drive release and A9 Main ACK are separate.
"""
from __future__ import annotations
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
STYLE=ROOT/"controls/latex/template"
PROFILES=ROOT/"registry/latex-build-profiles.json"

def sha(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for c in iter(lambda:f.read(2**20),b""):h.update(c)
    return h.hexdigest()

def run(cmd,cwd,env):
    p=subprocess.run(cmd,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if p.returncode:
        raise RuntimeError("BUILD TOOL FAILED: "+cmd[0]+"\n"+p.stdout[-2400:])
    return p.stdout

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--researcher",required=True,help="researcher slug or RSH-ID")
    ap.add_argument("--manifest",required=True,help="owner-approved machine source manifest JSON under repo")
    ap.add_argument("--mode",choices=("preview","exact-font-review"),default="preview")
    ap.add_argument("--output-dir",type=Path,required=True)
    ap.add_argument("--execute",action="store_true",help="required for ANY compile; dry run by default")
    args=ap.parse_args()
    profiles=json.loads(PROFILES.read_text())["profiles"]
    x=next((x for x in profiles if args.researcher in (x["researcher_id"],x["researcher_slug"])),None)
    if not x:ap.error("unknown researcher")
    manifest_path=(ROOT/args.manifest).resolve()
    if ROOT not in manifest_path.parents or not manifest_path.is_file():
        ap.error("manifest must be existing source-controlled file under repository")
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("researcher_id")!=x["researcher_id"] or manifest.get("build_authorized") is not True:
        ap.error("owning researcher ID or explicit build authorization missing")
    if manifest.get("source_admission")!="VERIFIED":
        ap.error("source admission is not VERIFIED")
    if manifest.get("selected_style")!="controls/latex/template/pumlsc-shared.sty":
        ap.error("project must inherit the single shared template")
    if manifest.get("citation_style") not in ("APA7","HARVARD","IEEE") or not manifest.get("document_stage"):
        ap.error("explicit citation style and approved document stage required")
    source=(ROOT/x["source_root"]).resolve()
    entry=(ROOT/x["entrypoint"]).resolve()
    if not source.is_dir() or not entry.is_file() or source not in entry.parents:
        ap.error("admitted source tree and main.tex not present")
    if r"\usepackage{pumlsc-shared}" not in entry.read_text(encoding="utf-8"):
        ap.error("manuscript does not import canonical shared style")
    if any(source.rglob("pumlsc-shared.sty")):
        ap.error("duplicated shared base is forbidden")
    if manifest.get("main_tex_sha256")!=sha(entry):
        ap.error("main.tex SHA256 differs from admitted source")
    target=args.output_dir.resolve()
    if ROOT==target or ROOT in target.parents:
        ap.error("derived outputs must be outside the repository")
    fontdir=None
    if args.mode=="exact-font-review":
        fontdir=Path(os.environ.get("RND_LATEX_FONT_DIR","")).expanduser()
        if not os.environ.get("RND_LATEX_FONT_DIR") or not fontdir.is_dir():
            ap.error("RND_LATEX_FONT_DIR licensed Times New Roman directory required")
        if not manifest.get("font_runtime_authorized"):
            ap.error("font runtime approval missing; cannot claim exact font")
    plan={"status":"DRY_RUN_NO_PDF" if not args.execute else "COMPILATION_REQUEST",
          "researcher_id":x["researcher_id"],"project_manifest":str(manifest_path.relative_to(ROOT)),
          "main_tex_sha256":sha(entry),"source_root":str(source.relative_to(ROOT)),
          "mode":args.mode,"steps":["xelatex","biber","xelatex","xelatex"],
          "automatic_github_compile":False,"scientific_release":"NOT_AUTHORIZED_HERE",
          "drive_upload":False,"a9_ack":False}
    if not args.execute:
        print(json.dumps(plan,indent=2));return
    for name in ("xelatex","biber","pdfinfo","pdffonts","pdftoppm","git"):
        if not shutil.which(name):ap.error("missing Linux build dependency "+name)
    if args.mode=="exact-font-review":
        for name in ("fc-match","fc-cache"):
            if not shutil.which(name):ap.error("missing fontconfig dependency "+name)
    with tempfile.TemporaryDirectory(prefix="rnd-latex-governed-") as td:
        work=Path(td)
        manuscript_dir=work/"manuscript"
        shutil.copytree(source,manuscript_dir)
        env=os.environ.copy()
        env["TEXINPUTS"]=str(STYLE)+os.pathsep+str(manuscript_dir)+os.pathsep+env.get("TEXINPUTS","")
        env["BIBINPUTS"]=str(manuscript_dir)+os.pathsep+env.get("BIBINPUTS","")
        if fontdir:
            conf=work/"fonts.conf"
            from xml.sax.saxutils import escape
            conf.write_text('<?xml version="1.0"?>\n<!DOCTYPE fontconfig SYSTEM "fonts.dtd">\n'
                '<fontconfig>\n<include ignore_missing="yes">/etc/fonts/fonts.conf</include>\n'
                '<dir>'+escape(str(fontdir.resolve()))+'</dir>\n'
                '<cachedir>'+escape(str(work/"font-cache"))+'</cachedir>\n</fontconfig>\n')
            env["FONTCONFIG_FILE"]=str(conf)
            run(["fc-cache","-f",str(fontdir.resolve())],manuscript_dir,env)
            match=run(["fc-match","-f",r"%{family}\n","Times New Roman"],manuscript_dir,env)
            if "Times New Roman" not in match:ap.error("fontconfig cannot resolve exact Times New Roman")
        cmd=["xelatex","-interaction=nonstopmode","-halt-on-error","-jobname=rnd-manuscript"]
        if args.mode=="preview":
            cmd.append(r"\def\PUPreviewTinosFont{1}\input{main.tex}")
        else:
            cmd.append("main.tex")
        run(cmd,manuscript_dir,env)
        run(["biber","rnd-manuscript"],manuscript_dir,env)
        run(cmd,manuscript_dir,env)
        run(cmd,manuscript_dir,env)
        built=manuscript_dir/"rnd-manuscript.pdf"
        if not built.is_file():raise RuntimeError("XeLaTeX produced no PDF")
        # Execute one shared machine PDF QA, including actual every-page rasterization.
        qa_script=ROOT/"scripts/latex/pdf_technical_qa.py"
        qa_mode="production" if args.mode=="exact-font-review" else "preview"
        qa_json=run([sys.executable,str(qa_script),"--pdf",str(built),"--mode",qa_mode,"--render","--json"],manuscript_dir,env)
        qa=json.loads(qa_json)
        log=(manuscript_dir/"rnd-manuscript.log").read_text(encoding="utf-8",errors="replace")
        if "undefined references" in log.lower() or "citation" in log.lower() and "undefined" in log.lower():
            raise RuntimeError("unresolved references or citations")
        if "overfull \\hbox" in log.lower() or "overfull \\vbox" in log.lower():
            raise RuntimeError("overfull boxes must be resolved in source")
        target.mkdir(parents=True,exist_ok=True)
        dest=target/("manuscript-tinos-preview.pdf" if args.mode=="preview" else "manuscript-exact-tnr-review.pdf")
        if dest.exists():raise RuntimeError("refusing to overwrite existing derived PDF")
        shutil.copy2(built,dest)
        plan.update({"status":"TECHNICAL_REVIEW_PDF_CREATED_NOT_SUBMISSION_FINAL",
                     "git_sha":run(["git","rev-parse","HEAD"],ROOT,env).strip(),
                     "pdf_sha256":sha(dest),"pdf_filename":dest.name,"pdf_qa":qa,
                     "scientific_approval":"HOLD","human_visual_review":"HOLD",
                     "university_144_rule_certification":"HOLD",
                     "drive_release":"NOT_PERFORMED","a9_main_ack":"NOT_PERFORMED"})
        report=target/"build-manifest.json"
        if report.exists():raise RuntimeError("build manifest already exists; refusing overwrite")
        report.write_text(json.dumps(plan,indent=2)+"\n",encoding="utf-8")
        print(json.dumps(plan,indent=2))
if __name__=="__main__":
    main()
