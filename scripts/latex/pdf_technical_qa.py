#!/usr/bin/env python3
"""No-edit PDF technical inspection for externally built thesis candidate.

Checks actual A4 dimensions and fonts; does not confer university/scientific
approval. Use --render to verify every page rasterizes; human visual QA still HOLD.
"""
import argparse,hashlib,json,re,shutil,subprocess,tempfile
from pathlib import Path
def run(args):
    p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:raise RuntimeError(args[0]+": "+p.stderr[-600:])
    return p.stdout
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--pdf",required=True,type=Path)
    ap.add_argument("--mode",choices=("preview","production"),required=True)
    ap.add_argument("--render",action="store_true")
    ap.add_argument("--json",action="store_true")
    args=ap.parse_args()
    f=args.pdf.resolve()
    if not f.is_file():ap.error("PDF not found")
    for tool in ("pdfinfo","pdffonts"):
        if not shutil.which(tool):ap.error(tool+" not installed")
    details=run(["pdfinfo",str(f)])
    match=re.search(r"Pages:\s+(\d+)",details);pages=int(match.group(1)) if match else 0
    per_page=run(["pdfinfo","-f","1","-l",str(pages),str(f)]) if pages else ""
    found=re.findall(r"Page\s+\d+\s+size:\s*([\d.]+)\s+x\s+([\d.]+)\s+pts",per_page)
    if not found:
        # pdfinfo may report only overall page size for uniform pages.
        found=re.findall(r"Page size:\s*([\d.]+)\s+x\s+([\d.]+)\s+pts",details)
    a4=bool(pages and found and all(
        (abs(float(x)-595.276)<1.1 and abs(float(y)-841.890)<1.1)
        or (abs(float(x)-841.890)<1.1 and abs(float(y)-595.276)<1.1)
        for x,y in found))
    fonts=run(["pdffonts",str(f)])
    exact_tnr=any(re.search(r"Times[+\- ]*New[+\- ]*Roman",line,re.I) and "yes" in line.lower()
                  for line in fonts.splitlines()[2:])
    raster=0
    if args.render:
        if not shutil.which("pdftoppm"):ap.error("pdftoppm unavailable")
        with tempfile.TemporaryDirectory(prefix="rnd-pdf-render-") as td:
            run(["pdftoppm","-f","1","-l",str(pages),"-r","85","-png",str(f),str(Path(td)/"page")])
            raster=len(list(Path(td).glob("page-*.png")))
    issues=[]
    if not a4:issues.append("A4 page-size verification FAILED")
    if args.mode=="production" and not exact_tnr:issues.append("Exact embedded Times New Roman NOT established")
    if args.render and raster!=pages:issues.append("Not all pages rasterized")
    digest=hashlib.sha256(f.read_bytes()).hexdigest()
    report={"classification":"TECHNICAL_CHECK_ONLY_NOT_PRODUCTION_CERTIFIED",
      "pdf_sha256":digest,"page_count":pages,"page_sizes_checked":len(found),
      "a4_dimensions_pass":a4,"exact_tnr_observed":exact_tnr,"pages_rasterized":raster,
      "mode":args.mode,"issues":issues,"human_visual_review":"HOLD","scientific_approval":"HOLD",
      "university_full_144_rule_certification":"HOLD","a9_main_ack":"NOT_PERFORMED"}
    print(json.dumps(report,indent=2) if args.json else "PDF TECHNICAL "+("HOLD" if issues else "PASS (NOT CERTIFIED)")+" "+json.dumps(report))
    if issues:raise SystemExit(2)
if __name__=="__main__":main()
