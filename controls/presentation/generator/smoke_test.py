from pathlib import Path
import subprocess, sys, json, hashlib
from PIL import Image, ImageDraw
here=Path(__file__).resolve().parent
out=here/"smoke_build"
# Build a temporary smoke theme whose expected logo hash is the generated non-scientific demo asset.
theme=json.loads((here/"theme.default.json").read_text())
logo=out/"smoke_logo.png"
out.mkdir(exist_ok=True)
im=Image.new("RGB",(220,220),"white")
ImageDraw.Draw(im).rectangle((3,3,216,216),outline="black",width=3)
im.save(logo)
smoke_content=json.loads((here/"content.example.json").read_text())
smoke_content["metadata"]["logo"]=str(logo)
smoke_content["metadata"]["logo_sha256"]=hashlib.sha256(logo.read_bytes()).hexdigest()
content_file=out/"content.smoke.json"
content_file.write_text(json.dumps(smoke_content,indent=2))
h=hashlib.sha256(logo.read_bytes()).hexdigest()
theme["branding"]["canonical_logo_sha256"]=h
smoke_theme=here/"theme.smoke.json"
smoke_theme.write_text(json.dumps(theme,indent=2))
cmd=[sys.executable,str(here/"build.py"),"--content",str(content_file),"--theme",str(smoke_theme),"--out-dir",str(out),"--fixture"]
r=subprocess.run(cmd,capture_output=True,text=True)
print(r.stdout)
if r.returncode:
    print(r.stderr,file=sys.stderr)
    raise SystemExit(r.returncode)
required=["presentation.pdf","presentation.pptx","validation.json","semantic_validation.json","qa_release.json","release_manifest.json","montage.jpg"]
missing=[x for x in required if not (out/x).exists()]
if missing: raise SystemExit(f"missing outputs: {missing}")
v=json.loads((out/"validation.json").read_text())
if not v["ok"]: raise SystemExit(v)
m=json.loads((out/"release_manifest.json").read_text())
if float(m.get("title_logo_size_in",0)) < 2.25: raise SystemExit("title logo gate not recorded")
if not m.get("supervisor_present"): raise SystemExit("supervisor gate not recorded")
if int(m.get("co_supervisor_count",0)) < 1: raise SystemExit("co-supervisor gate not recorded")
print("SMOKE_TEST_PASS_CANDIDATE_SEMANTIC_V2_2")
