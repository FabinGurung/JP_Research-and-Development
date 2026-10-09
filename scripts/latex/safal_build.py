#!/usr/bin/env python3
"""Safal source-admission gate and controlled local XeLaTeX/Biber compilation.
Never uploads to Drive, commits fonts, or claims scientific approval.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
CONTROL=ROOT/"controls/projects/safal-dawadi.latex.json"  # historical evidence and build metadata only
CANONICAL=ROOT/"controls/latex/tower.json"
SHARED=ROOT/"controls/latex/template/pumlsc-shared.sty"
RESEARCHER_CONFIG=ROOT/"researchers/safal-dawadi/latex/control.json"
FONT_FILES=("times.ttf","timesbd.ttf","timesi.ttf","timesbi.ttf")

def fail(msg):
    raise SystemExit("SAFAL LATEX HOLD/FAIL: "+msg)

def checksum(path):
    h=hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda:fh.read(2**20),b""):
            h.update(chunk)
    return h.hexdigest()

def invoke(cmd,cwd,env):
    proc=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,errors="replace")
    print("QA_RUN",cmd[0],"returncode",proc.returncode)
    if proc.returncode!=0:
        print(proc.stdout[-2000:])
        fail("tool failed: "+cmd[0])
    return proc.stdout

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--mode",choices=("check","compile"),default="check")
    p.add_argument("--output-dir",help="Private temporary candidate output directory for manual publication review")
    args=p.parse_args()
    tower=json.loads(CANONICAL.read_text(encoding="utf-8"))
    configured=json.loads(RESEARCHER_CONFIG.read_text(encoding="utf-8"))
    if tower.get("control_id")!="RD-CONTROL-LATEX-001" or configured.get("shared_control")!="controls/latex/tower.json":
        fail("missing or divergent SINGLE shared LaTeX authority")
    if configured.get("shared_template")!="controls/latex/template/pumlsc-shared.sty" or not SHARED.is_file():
        fail("shared LaTeX template missing or researcher source not linked")
    c=json.loads(CONTROL.read_text(encoding="utf-8"))
    if c.get("researcher_id")!="RSH-010":
        fail("wrong researcher")
    g=c["gates"]
    if any(g.get(k)!="VERIFIED" for k in ("source_reconciliation","public_git_clearance","source_admission")):
        if args.mode=="check":
            print("SOURCE_GATE=HOLD_NOT_ADMITTED; NO_THESIS_PDF_COMPILED; NO_DRIVE_WRITE")
            return
        fail("verified reconciled and privacy-cleared Git source has not been admitted")
    source=ROOT/c["build"]["source_root"]
    entry=source/"manuscript/main.tex"
    # Central shared template must be loaded in any admitted manuscript.
    # Never copy the shared style to the researcher directory.
    for stray in source.rglob("pumlsc-shared.sty"):
        fail("duplicated shared template in researcher source: "+str(stray.relative_to(ROOT)))
    if not entry.is_file(): fail("admitted Git main.tex not found")
    if r"\\usepackage{pumlsc-shared}" not in entry.read_text(encoding="utf-8"):
        fail("admitted source must import canonical pumlsc-shared package")
    if args.mode=="check":
        print("SOURCE_GATE=SOURCE_PRESENT__NO_THESIS_PDF_COMPILED")
        return
    if g.get("exact_font_ci")!="VERIFIED":
        fail("exact licensed font environment not yet validated")
    fdir=os.environ.get("SAFAL_FONT_DIR","")
    if not fdir or any(not (Path(fdir)/n).is_file() for n in FONT_FILES):
        fail("private licensed Times New Roman assets are missing")
    for tool in ("xelatex","biber","pdfinfo","pdffonts","pdftoppm"):
        if shutil.which(tool) is None: fail("missing compiler or PDF QA tool: "+tool)
    if not args.output_dir: fail("explicit --output-dir is required, not a repository directory")
    out=Path(args.output_dir).resolve()
    if out==ROOT or ROOT in out.parents:
        fail("compiled PDFs and sensitive build output cannot be stored inside tracked public repository")
    with tempfile.TemporaryDirectory(prefix="safal-restricted-build-") as t:
        work=Path(t)
        tree=work/"project"
        shutil.copytree(source,tree)
        texdir=tree/"manuscript"
        # Private licensed assets exist only in ephemeral work directory, never Git history or public artifacts.
        for n in FONT_FILES:
            shutil.copy2(Path(fdir)/n,texdir/n)
        env=os.environ.copy()
        env["TEXINPUTS"]=str(SHARED.parent)+os.pathsep+str(tree)+os.pathsep+str(tree/"bibliography")+os.pathsep+env.get("TEXINPUTS","")
        env["BIBINPUTS"]=str(tree/"bibliography")+os.pathsep+env.get("BIBINPUTS","")
        sequence=[
            ["xelatex","-interaction=nonstopmode","-halt-on-error","main.tex"],
            ["biber","main"],
            ["xelatex","-interaction=nonstopmode","-halt-on-error","main.tex"],
            ["xelatex","-interaction=nonstopmode","-halt-on-error","main.tex"]]
        for cmd in sequence: invoke(cmd,texdir,env)
        pdf=texdir/"main.pdf"
        if not pdf.is_file(): fail("missing compiled main.pdf")
        pdfinfo=invoke(["pdfinfo",str(pdf)],texdir,env)
        if not re.search(r"Page size:\s+595(?:\.\d+)?\s+x\s+842",pdfinfo):
            fail("PDF not verified as A4; do not assume exact university format")
        fontinfo=invoke(["pdffonts",str(pdf)],texdir,env)
        if not re.search(r"Times",fontinfo,re.I):
            fail("Times New Roman embedding was not established")
        log=(texdir/"main.log").read_text(errors="replace")
        if "undefined references" in log.lower() or re.search(r"citation .* undefined",log,re.I):
            fail("unresolved citations/references")
        if "overfull \\hbox" in log.lower(): fail("overfull boxes detected")
        # Render every page to enforce basic renderability; detailed human visual QA remains a separate hold.
        pages=re.search(r"Pages:\s+(\d+)",pdfinfo)
        if not pages: fail("unknown PDF page count")
        render=work/"render";render.mkdir()
        invoke(["pdftoppm","-jpeg","-scale-to","850",str(pdf),str(render/"page")],texdir,env)
        if len(list(render.glob("page-*.jpg")))!=int(pages.group(1)):
            fail("full-page PDF render count mismatch")
        out.mkdir(parents=True,exist_ok=True)
        dest=out/"safal-technical-review-candidate.pdf"
        shutil.copy2(pdf,dest)
        sha=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
        report={"status":"TECHNICAL_QA_CANDIDATE__HUMAN_VISUAL_AND_PU_FULL_COMPLIANCE_PENDING",
                "git_commit":sha,"researcher_id":"RSH-010","manuscript_version":c["manuscript"]["version"],
                "pdf_sha256":checksum(dest),"source_main_tex_sha256":checksum(entry),
                "pdf_page_count":int(pages.group(1)),"pdf_drive_id":None,"a9_local_seq":None,
                "scientific_approval":"HOLD","publication_status":"NOT_UPLOADED_TO_GOOGLE_DRIVE"}
        (out/"build-manifest.json").write_text(json.dumps(report,indent=2)+"\n")
        print("TECHNICAL_BUILD_CANDIDATE: no Drive publication, no human science approval")
if __name__=="__main__":
    main()
