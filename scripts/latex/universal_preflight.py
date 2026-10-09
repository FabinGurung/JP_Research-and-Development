#!/usr/bin/env python3
"""Universal thesis source gate and deterministic build PLAN. NO automatic compilation.

Pass explicit --researcher and --manifest to inspect one project; all other
theses remain untouched. Production authorization is independent of source QA.
"""
from __future__ import annotations
import argparse,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
POL=ROOT/"registry/latex-build-profiles.json"
ROUTES=ROOT/"controls/latex/pu-rule-enforcement-matrix.json"
TOWER=ROOT/"controls/latex/tower.json"
STY=ROOT/"controls/latex/template/pumlsc-shared.sty"
def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def canonical(path):
    p=(ROOT/path).resolve()
    if p!=ROOT and ROOT not in p.parents: raise ValueError("outside repository: "+str(path))
    return p
def policy_validation():
    prof=load(POL); route=load(ROUTES); tower=load(TOWER)
    people=load(ROOT/"registry/researchers.json")["researchers"]
    known={(r["researcher_id"],r["slug"]) for r in people}
    actual={(p["researcher_id"],p["researcher_slug"]) for p in prof["profiles"]}
    errors=[]
    if known!=actual or len(actual)!=len(prof["profiles"]):errors.append("researcher build profiles incomplete")
    if prof["canonical_style"]!="controls/latex/template/pumlsc-shared.sty" or not STY.is_file():errors.append("canonical shared template drift")
    if tower.get("authority_path")!="controls/latex/tower.json":errors.append("competing tower")
    source_audit=load(ROOT/"controls/latex/pu-format-parity-audit.json")
    a={x["id"] for x in source_audit["per_rule"]}; b={x["id"] for x in route["rules"]}
    if len(a)!=144 or a!=b:errors.append("144 PU rules not fully classified")
    if any(x.get("certification_status")!="NOT_UNIVERSALLY_CERTIFIED" for x in route["rules"]):errors.append("unearned full PU certification")
    if any(x.get("compile_on_push") for x in prof["profiles"]):errors.append("researcher automatic scientific compile enabled")
    return errors
def inspect_one(profile,manifest_path):
    problems=[]
    entry=canonical(profile["entrypoint"])
    source_dir=canonical(profile["source_root"])
    if not entry.is_file():
        problems.append("HOLD: no verified active source main.tex at "+str(entry.relative_to(ROOT)))
    elif r"\usepackage{pumlsc-shared}" not in entry.read_text(encoding="utf-8"):
        problems.append("HOLD: main.tex does not import the single shared package")
    if source_dir.is_dir() and list(source_dir.rglob("pumlsc-shared.sty")):
        problems.append("HOLD: forbidden cloned shared style")
    if manifest_path is None:
        problems.append("HOLD: exact owning project manifest not supplied")
    else:
        manifest=load(canonical(manifest_path))
        if manifest.get("researcher_id")!=profile["researcher_id"]:
            problems.append("HOLD: project manifest researcher mismatch")
        if manifest.get("source_admission")!="VERIFIED":
            problems.append("HOLD: source admission must be VERIFIED")
        if manifest.get("selected_style")!="controls/latex/template/pumlsc-shared.sty":
            problems.append("HOLD: project cannot fork shared style")
        if manifest.get("citation_style") not in ("APA7","HARVARD","IEEE"):
            problems.append("HOLD: explicitly choose APA7/HARVARD/IEEE")
        if not manifest.get("document_stage"):
            problems.append("HOLD: missing verified document stage")
        if entry.is_file() and manifest.get("main_tex_sha256"):
            digest=hashlib.sha256(entry.read_bytes()).hexdigest()
            if digest!=manifest["main_tex_sha256"]:
                problems.append("HOLD: main.tex hash differs from admitted source manifest")
    return problems
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--policy-check",action="store_true",help="validate 11 registered build profiles and all PU rule IDs")
    ap.add_argument("--researcher",help="RSH ID or slug")
    ap.add_argument("--manifest",help="owning project's source admission and build config JSON")
    ap.add_argument("--json",action="store_true")
    a=ap.parse_args()
    errors=policy_validation()
    if errors:
        print("UNIVERSAL POLICY FAIL: "+"; ".join(errors));sys.exit(1)
    if a.policy_check:
        print("UNIVERSAL SOURCE POLICY PASS (144 indexed; zero new PDF certification; no auto builds)")
        return
    if not a.researcher:ap.error("--researcher or --policy-check required")
    profiles=load(POL)["profiles"]
    profile=next((p for p in profiles if a.researcher in (p["researcher_id"],p["researcher_slug"])),None)
    if not profile:ap.error("unknown researcher")
    problems=inspect_one(profile,a.manifest)
    result={"researcher_id":profile["researcher_id"],"status":"HOLD" if problems else "SOURCE_PREFLIGHT_PASS_ONLY",
      "reasons":problems,"automatic_compilation":False,
      "build_plan":["xelatex","biber","xelatex","xelatex"],
      "template":"controls/latex/template/pumlsc-shared.sty","scientific_approval":"NOT_TESTED",
      "pdf":None,"note":"This tool does not compile a PDF, change Drive or register A9 Main."}
    if a.json:print(json.dumps(result,indent=2))
    else:print(result["status"]+": "+"; ".join(problems or ["source preflight only; no PDF generated"]))
    if problems:sys.exit(2)
if __name__=="__main__":main()
