#!/usr/bin/env python3
from __future__ import annotations
import argparse, html, json, shutil
from pathlib import Path
from urllib.parse import quote

ROOT=Path(__file__).resolve().parents[1]
REPO_URL="https://github.com/FabinGurung/JP_Research-and-Development"
SITE_URL="https://fabingurung.github.io/JP_Research-and-Development/"

def load(path): return json.loads((ROOT/path).read_text(encoding="utf-8"))
def esc(v): return html.escape("" if v is None else str(v))
def branch_url(branch): return f"{REPO_URL}/tree/{quote(branch, safe='/')}"
def drive_url(file_id):
    return f"https://drive.google.com/open?id={file_id}" if file_id else None

def shell(title, body, depth=0):
    prefix="../"*depth
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · JP R&D</title><link rel="stylesheet" href="{prefix}assets/styles.css"></head><body><header class="topbar"><div class="wrap nav"><strong>JP R&D</strong><nav class="navlinks"><a href="{prefix}index.html">Home</a><a href="{prefix}researchers/index.html">Researchers</a><a href="{prefix}workspace/index.html">Workspace</a><a href="{prefix}controls/index.html">Controls</a><a href="{prefix}how-to/index.html">How to</a></nav></div></header>{body}<footer class="wrap footer">JP Research & Development · code + controls + pointers · working artifacts remain in Google Drive.</footer></body></html>"""

def write(out, rel, content):
    p=out/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content,encoding="utf-8")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",default="dist"); args=ap.parse_args()
    out=ROOT/args.out
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    researchers=load(Path("registry/researchers.json"))["researchers"]
    branches=load(Path("registry/branch-registry.json"))
    policy=load(Path("controls/repository.control.json"))
    controls={
      "Discussion":load(Path("controls/discussion.control.json")),
      "LaTeX":load(Path("controls/latex.control.json")),
      "Presentation":load(Path("controls/presentation.control.json"))
    }
    (out/"assets").mkdir(); shutil.copy2(ROOT/"web/styles.css",out/"assets/styles.css")
    (out/".nojekyll").write_text("",encoding="utf-8")
    home_cards="".join(f'<article class="card"><span class="badge">ON HOLD · HUMAN QA</span><h3>{esc(r["display_name"])}</h3><p>Topic/title and Drive pointers are intentionally unset.</p><a href="researchers/{esc(r["slug"])}/index.html">Open researcher workspace →</a></article>' for r in researchers)
    home=f'''<main><section class="wrap hero"><div class="eyebrow">Research control portal</div><h1>JP Research & Development</h1><p class="lead">One thin main branch for shared controls, researcher routing and verified Drive links. Research documents and generated outputs stay in Google Drive; source code lives in governed researcher lanes.</p><p><span class="badge">9 researcher pages on QA hold</span></p></section><section class="wrap section"><h2>Operating architecture</h2><div class="flow"><div class="node">Shared controls</div><div class="arrow">→</div><div class="node">Researcher index</div><div class="arrow">→</div><div class="node">Discussion / LaTeX / Presentation lanes</div><div class="arrow">→</div><div class="node">Google Drive outputs</div></div></section><section class="wrap section"><h2>Researchers</h2><div class="grid">{home_cards}</div></section><section class="wrap section"><h2>Boundaries</h2><div class="controls"><article class="card"><h3>GitHub main</h3><p>Portal code, controls, schemas, registries and links only.</p></article><article class="card"><h3>Researcher branches</h3><p>Discussion pointers, LaTeX source, presentation source/config.</p></article><article class="card"><h3>Google Drive</h3><p>Working Docs, compiled PDFs, generated PPTX/PDF and evidence.</p></article></div></section></main>'''
    write(out,"index.html",shell("Home",home,0))
    directory="".join(f'<article class="card"><h3>{esc(r["display_name"])}</h3><p><span class="badge">HOLD_HUMAN_QA</span></p><p>Topic short name: <strong>ON HOLD</strong></p><a href="{esc(r["slug"])}/index.html">Open →</a></article>' for r in researchers)
    write(out,"researchers/index.html",shell("Researchers",f'<main class="wrap hero"><div class="eyebrow">Researcher index</div><h1>Researcher workspaces</h1><p class="lead">No topic/title is published until human QA verifies it.</p><div class="grid">{directory}</div></main>',1))
    for r in researchers:
        lane_html=""
        for key,label in [("discussion","Discussion"),("latex","LaTeX"),("presentation","Presentation")]:
            lane=r["lanes"][key]
            lane_html+=f'<article class="lane"><h3>{label}</h3><div class="code">{esc(lane["branch"])}</div><p class="muted">{esc(lane["content_policy"])}</p><a href="{branch_url(lane["branch"])}">Open Git branch →</a></article>'
        drive=r["drive"]
        rows=[
          ("Discussion Google Doc",drive.get("discussion_google_doc_id")),
          ("Working thesis PDF",drive.get("working_pdf_drive_id")),
          ("Presentation PDF",drive.get("presentation_pdf_drive_id")),
          ("Presentation PPTX",drive.get("presentation_pptx_drive_id")),
        ]
        links="".join(f'<div>{esc(label)}</div><div>{f"""<a href="{drive_url(fid)}">Open Drive file</a>""" if fid else """<span class="badge">ON HOLD</span>"""}</div>' for label,fid in rows)
        body=f'''<main class="wrap hero"><div class="eyebrow">{esc(r["researcher_id"])}</div><h1>{esc(r["display_name"])}</h1><p><span class="badge">HOLD · HUMAN QA REQUIRED</span></p><div class="notice">Research topic, title, short page name and all Drive file IDs are intentionally unpublished until human QA.</div><section class="section"><h2>Topic</h2><div class="kvs"><div>Title</div><div>ON HOLD</div><div>Short name</div><div>ON HOLD</div></div></section><section class="section"><h2>Research lanes</h2><div class="lanes">{lane_html}</div></section><section class="section"><h2>Google Drive outputs</h2><div class="kvs">{links}</div></section></main>'''
        write(out,f'researchers/{r["slug"]}/index.html',shell(r["display_name"],body,2))
    workspace=f'''<main class="wrap hero"><div class="eyebrow">Repository field</div><h1>Workspace</h1><p class="lead">This repository is a code-and-pointer control plane for R&D. It is not the document warehouse.</p><section class="section"><div class="kvs"><div>Main</div><div>Portal code, shared controls, researcher registry, schemas, Drive/GitHub pointers.</div><div>Discussion lane</div><div>Google Doc ID/link and automation metadata only; discussion prose remains in Drive.</div><div>LaTeX lane</div><div>.tex/.bib/build code; compiled PDF is uploaded to Drive.</div><div>Presentation lane</div><div>TypeScript/PptxGenJS/YAML/JSON/HTML/CSS/SVG; generated PPTX/PDF is uploaded to Drive.</div><div>Archive</div><div>Git history plus legacy branches classified read-only.</div></div></section><section class="section"><h2>Branch state</h2><p>{len(branches["archived_legacy"])} legacy refs are classified <strong>ARCHIVED_LEGACY</strong>. The new model defines {len(branches["active_researcher_lanes"])} researcher lane branches.</p></section></main>'''
    write(out,"workspace/index.html",shell("Workspace",workspace,1))
    cards=""
    for name,c in controls.items():
        slug=name.lower().replace("latex","latex")
        cards+=f'<article class="card"><h3>{name}</h3><p>Control ID: <span class="code">{esc(c["control_id"])}</span></p><a href="{slug}/index.html">Open control →</a></article>'
    write(out,"controls/index.html",shell("Controls",f'<main class="wrap hero"><div class="eyebrow">Shared control towers</div><h1>One format for every researcher</h1><p class="lead">Researcher lanes inherit these contracts so ChatGPT does not invent a new workflow per researcher.</p><div class="controls">{cards}</div></main>',1))
    for name,c in controls.items():
        slug=name.lower()
        body=f'<main class="wrap hero"><div class="eyebrow">Shared control</div><h1>{name}</h1><div class="kvs"><div>Control ID</div><div class="code">{esc(c["control_id"])}</div><div>Status</div><div>{esc(c["status"])}</div><div>Branch pattern</div><div class="code">{esc(c["branch_pattern"])}</div><div>Authority</div><div>{esc(c["authority"])}</div></div><section class="section"><h2>Workflow</h2><ol>'+''.join(f'<li>{esc(x)}</li>' for x in c["workflow"])+'</ol></section></main>'
        write(out,f"controls/{slug}/index.html",shell(name,body,2))
    how=f'''<main class="wrap hero"><div class="eyebrow">ChatGPT operating path</div><h1>How to use this repository</h1><section class="section"><div class="flow"><div class="node">Choose researcher</div><div class="arrow">→</div><div class="node">Choose lane</div><div class="arrow">→</div><div class="node">Read shared control</div><div class="arrow">→</div><div class="node">Work in branch</div></div></section><section class="section"><h2>External output flow</h2><p class="lead">Build/render → upload output to Google Drive → read back the Drive ID/link → update the lane pointer JSON → commit. Git commit history replaces routine duplicate PRE/POST archive copies.</p></section><section class="section"><h2>Presentation recommendation</h2><p>Default to <strong>TypeScript + PptxGenJS + YAML/JSON</strong> for editable presentations. HTML/CSS/SVG may be used for PDF-first rendering. Generated PPTX/PDF files belong in Drive, not Git.</p></section></main>'''
    write(out,"how-to/index.html",shell("How to",how,1))
    data_dir=out/"data"; data_dir.mkdir()
    for src,name in [(ROOT/"registry/researchers.json","researchers.json"),(ROOT/"registry/branch-registry.json","branch-registry.json"),(ROOT/"controls/repository.control.json","repository-policy.json")]:
        shutil.copy2(src,data_dir/name)
    print(f"built {out} researchers={len(researchers)}")

if __name__=="__main__": main()
