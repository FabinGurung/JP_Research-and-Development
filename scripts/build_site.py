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

def evidence_html(debt):
    parts=[]
    for e in debt.get("evidence",[]):
        u=drive_url(e.get("drive_id")) if e.get("drive_id") else e.get("url")
        if not u or not str(u).startswith("https://"):
            continue
        parts.append(f'<li>{esc(e.get("role"))}: <a href="{esc(u)}">Open evidence</a></li>')
    return "".join(parts) or "<li>No external evidence pointer required.</li>"

def shell(title, body, depth=0):
    prefix="../"*depth
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · JP R&D</title><link rel="stylesheet" href="{prefix}assets/styles.css"><script defer src="{prefix}assets/theme.js"></script><script defer src="{prefix}assets/motion.js"></script></head><body><header class="topbar"><div class="wrap nav"><strong>JP R&D</strong><nav class="navlinks"><a href="{prefix}index.html">Home</a><a href="{prefix}researchers/index.html">Researchers</a><a href="{prefix}thesis-infrastructure/index.html">Thesis folders</a><a href="{prefix}workspace/index.html">Workspace</a><a href="{prefix}controls/index.html">Controls</a><a href="{prefix}debts/index.html">Debts</a><a href="{prefix}roadmap/index.html">Roadmap</a><a href="{prefix}branches/index.html">Branches</a><a href="{prefix}how-to/index.html">How to</a><button type="button" class="theme-switch" data-theme-toggle aria-label="Switch to mauve dusk">☾ Dusk palette</button></nav></div></header>{body}<footer class="wrap footer">JP Research & Development · code + controls + pointers · working artifacts remain in Google Drive.</footer></body></html>"""

def write(out, rel, content):
    p=out/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content,encoding="utf-8")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",default="dist"); args=ap.parse_args()
    out=ROOT/args.out
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    researchers=load(Path("registry/researchers.json"))["researchers"]
    folder_roles=load(Path("registry/researcher-folder-roles.json"))
    owner_status=load(Path("registry/researcher-migration-status.json"))
    owner_by_id={x["researcher_id"]:x for x in owner_status["records"]}
    folder_by_slug={x["researcher_slug"]:x for x in folder_roles["records"]}
    websites=load(Path("registry/websites.json"))["websites"]
    branches=load(Path("registry/branch-registry.json"))
    policy=load(Path("controls/repository.control.json"))
    controls={
      "Discussion":load(Path("controls/discussion.control.json")),
      "LaTeX":load(Path("controls/latex/tower.json")),
      "Presentation":load(Path("controls/presentation.control.json")),
      "Website":load(Path("controls/website.control.json"))
    }
    debts=load(Path("registry/debts.json"))["debts"]
    manoj_audit=load(Path("registry/drive-audits/02-thesis/manoj-bhandari.json"))
    avishek_audit=load(Path("registry/drive-audits/02-thesis/avishek-kumar-mandal.json"))
    root_rescan=load(Path("registry/drive-audits/02-thesis/root-rescan-20261008.json"))
    batch_audits={
        slug:load(Path(f"registry/drive-audits/02-thesis/{slug}.json"))
        for slug in ("rural-road-maintenance","safal-dawadi","saugat-paneru","nabin-bista","krishna-kumar-gupta","shisheer-kc","sunil-rana","fabin-gurung","master-index")
    }
    (out/"assets").mkdir(); shutil.copy2(ROOT/"web/styles.css",out/"assets/styles.css"); shutil.copy2(ROOT/"web/theme.js",out/"assets/theme.js"); shutil.copy2(ROOT/"web/branches.js",out/"assets/branches.js"); shutil.copy2(ROOT/"web/motion.js",out/"assets/motion.js")
    (out/".nojekyll").write_text("",encoding="utf-8")
    # Restore the original public-safe standalone demos into the ONE main Pages deployment.
    # Source blobs retain the archived Git IDs and are immutable until separately revised.
    legacy=ROOT/"web/legacy-site"
    for site_name in ("methodology-demo","hydropower-data-model","hydropower-data-schema","hydropower-data-tables","hydropower-data-graph","hydropower-nepal-map"):
        src=legacy/site_name
        if src.is_dir(): shutil.copytree(src,out/site_name,dirs_exist_ok=True)
    home_cards="".join(f'<article class="card"><span class="badge">{esc("TITLE VERIFIED · OTHER POINTERS HOLD" if r["qa_status"]=="TITLE_VERIFIED_OTHER_POINTERS_HOLD" else "ON HOLD · HUMAN QA")}</span><h3>{esc(r["display_name"])}</h3><p>{esc(r.get("topic_title") or "Topic/title and Drive pointers are intentionally unset.")}</p><a href="researchers/{esc(r["slug"])}/index.html">Open researcher workspace →</a></article>' for r in researchers)
    home=f'''<main><section class="wrap hero"><div class="eyebrow">Research control portal</div><h1>JP Research & Development</h1><p class="lead">One thin main branch for shared controls, researcher routing and verified Drive links. Research documents and generated outputs stay in Google Drive; code changes are tracked on full-repository Git branches; researcher paths are logical work areas.</p><p><span class="badge">{len(researchers)} researcher workspaces · selective human QA</span></p></section><section class="wrap section"><h2>Operating architecture</h2><div class="flow"><div class="node">Shared controls</div><div class="arrow">→</div><div class="node">Researcher index</div><div class="arrow">→</div><div class="node">Discussion / LaTeX / Presentation lanes</div><div class="arrow">→</div><div class="node">Google Drive outputs</div></div></section><section class="wrap section"><h2>Researchers</h2><div class="grid">{home_cards}</div></section><section class="wrap section"><h2>Boundaries</h2><div class="controls"><article class="card"><h3>GitHub main</h3><p>Portal code, controls, schemas, registries and links only.</p></article><article class="card"><h3>Researcher branches</h3><p>Discussion pointers, LaTeX source, presentation source/config.</p></article><article class="card"><h3>Google Drive</h3><p>Working Docs, compiled PDFs, generated PPTX/PDF and evidence.</p></article></div></section></main>'''
    old_intro_start=home.index('<section class="wrap hero">')
    old_intro_end=home.index("</section>",old_intro_start)+len("</section>")
    new_intro=(ROOT/"web/living-hero.html").read_text(encoding="utf-8")
    new_intro=new_intro.replace("@@RESEARCHERS@@",str(len(researchers))).replace("@@ROOTS@@",str(folder_roles["verified_root_count"]))
    home=home[:old_intro_start]+new_intro+home[old_intro_end:]
    home=home.replace("</main>",'<section class="wrap section"><h2>Unified thesis infrastructure</h2><p>Browse verified project folder roles, source-control policy, university formatting engine and individual researcher handovers. No Drive folders were renamed or moved.</p><p><a href="thesis-infrastructure/index.html">Open thesis folder and automation map →</a></p></section></main>')
    write(out,"index.html",shell("Home",home,0))
    roadmap=load(Path("registry/roadmap.json"))
    def stage_cards(items,kind):
        return "".join(
          '<article class="card"><span class="badge">'+esc(x.get("status",x.get("state","OPEN")))+'</span>'
          +'<h3>'+esc(x["title"])+'</h3>'
          +'<p>'+esc(x.get("detail",x.get("done_when","")))+'</p>'
          +(('<p class="muted">'+esc(x.get("priority",""))+'</p>') if kind=="next" else "")
          +'</article>' for x in items
        )
    delivered=stage_cards(roadmap["developed"],"done")
    pending=stage_cards(roadmap["next"],"next")
    holds="".join('<li><strong>'+esc(x["id"])+'</strong> — '+esc(x["state"])+': '+esc(x["reason"])+'</li>' for x in roadmap["holds"])
    counterpart=roadmap["governance"]["linked_a7_roadmap"]
    roadmap_body=(
      '<main class="wrap hero"><div class="eyebrow">R&D · canonical development history and delivery roadmap</div>'
      '<h1>What we built, and what comes next</h1>'
      '<p class="lead">Point-in-time audit: 18/18 Drive direct children, 11 researchers, 33 whole-repository Git work refs, two Fabin research modules and six historical static demo directories. A folder audit is not final thesis approval.</p>'
      '<p><a href="'+esc(counterpart)+'">Open the A7 global control-plane roadmap →</a></p>'
      '<section class="section"><h2>Delivered</h2><div class="grid">'+delivered+'</div></section>'
      '<section class="section"><h2>Prioritized next work</h2><div class="grid">'+pending+'</div></section>'
      '<section class="section"><h2>Holds and debts that must stay visible</h2><ul>'+holds+'</ul></section>'
      '<section class="section"><h2>Durable handover</h2><p><a href="https://github.com/FabinGurung/JP_Research-and-Development/blob/main/docs/HANDOVER_TO_A7_20261009.md">Cross-thread handover for A7 →</a></p>'
      '<p><a href="https://github.com/FabinGurung/JP_Research-and-Development/blob/main/registry/roadmap.json">Machine-readable roadmap source →</a></p></section></main>'
    )
    write(out,"roadmap/index.html",shell("R&D Roadmap",roadmap_body,1))
    # Every observed Git branch (including legacy, template, source and rollback refs).
    branch_inventory=load(Path("registry/branch-inventory.json"))
    branch_rows=branch_inventory["branches"]
    branch_groups=branch_inventory["counts"]
    category_options="".join(f'<option value="{esc(k)}">{esc(k.replace("-"," ").title())} ({v})</option>' for k,v in sorted(branch_groups.items()))
    branch_table_rows="".join(
        '<tr data-branch-row data-category="'+esc(b["category"])+'" data-search="'+esc(" ".join((b["name"],b["category"],b["purpose"],b.get("primary_source_path") or "",b["source_status"])).lower())+'">'
        +'<td><a href="'+esc(branch_url(b["name"]))+'"><strong>'+esc(b["name"])+'</strong></a></td>'
        +'<td><span class="branch-pill">'+esc(b["category"])+'</span></td>'
        +'<td class="branch-description">'+esc(b["purpose"])+'</td>'
        +'<td class="code">'+esc(b.get("primary_source_path") or "—")+'</td>'
        +'<td><a class="code" title="'+esc(b["commit_sha"])+'" href="'+esc(REPO_URL+"/commit/"+b["commit_sha"])+'">'+esc(b["commit_sha"][:10])+'</a></td></tr>'
        for b in branch_rows
    )
    branch_body=(
        '<main class="wrap hero"><div class="eyebrow">Whole-repository Git source · audited branch refs</div>'
        '<h1>Every branch. Every purpose.</h1>'
        '<p class="lead">All '+str(len(branch_rows))+' branches observed on '+esc(branch_inventory["observed_date"])+'. Search each full name, role, purpose, source path and exact commit. This is a provider snapshot; GitHub live refs must be reread before a change.</p>'
        '<div class="notice">The 33 researcher branches still point to shared template code, not individual admitted thesis sources. The new <code>resource/**/v001</code> branches contain the updated whole-repository codebase and scoped source manifests. Original archived references have not been rewritten.</div>'
        '<section class="section"><div class="branch-toolbar">'
        '<label>Find branch<input id="branch-search" type="search" placeholder="Search researcher, source, snapshot, commit…" autocomplete="off"></label>'
        '<label>Branch type<select id="branch-category"><option value="">All categories</option>'+category_options+'</select></label>'
        '<span class="branch-count" id="branch-visible" aria-live="polite">'+str(len(branch_rows))+' / '+str(len(branch_rows))+' branches</span>'
        '</div><div class="branch-table-wrap"><table class="branch-table"><thead><tr><th>Git branch</th><th>Type</th><th>Intended use and actual status</th><th>Source path</th><th>Observed SHA</th></tr></thead><tbody>'+branch_table_rows+'</tbody></table></div>'
        '<p><a href="https://github.com/FabinGurung/JP_Research-and-Development/blob/main/registry/branch-inventory.json">Open machine-readable complete branch inventory →</a> · '
        '<a href="https://github.com/FabinGurung/JP_Research-and-Development/blob/main/docs/BRANCH_VERSIONING_AND_INVENTORY.md">Open versioning and rollback rule →</a></p>'
        '</section></main>'
    )
    write(out,"branches/index.html",shell("Every Git Branch",branch_body+'<script defer src="../assets/branches.js"></script>',1))
    home=home.replace("</main>",'<section class="wrap section"><h2>Code, branches and version history</h2><p class="lead">Search '+str(len(branch_rows))+' audited branches, their intended use, code paths and immutable commit snapshots. The single website is built from <code>main</code>.</p><p><a href="branches/index.html">Browse all Git branches →</a></p></section></main>')
    write(out,"index.html",shell("Home",home,0))
    directory="".join(f'<article class="card"><h3>{esc(r["display_name"])}</h3><p><span class="badge">{esc(r["qa_status"])}</span></p><p>{esc(r.get("topic_title") or "Topic title: ON HOLD")}</p><a href="{esc(r["slug"])}/index.html">Open →</a></article>' for r in researchers)
    directory='<p><a href="../thesis-infrastructure/index.html">Explore normalized thesis folder roles and stable Drive IDs →</a></p>'+directory
    write(out,"researchers/index.html",shell("Researchers",f'<main class="wrap hero"><div class="eyebrow">Researcher index</div><h1>Researcher workspaces</h1><p class="lead">No topic/title is published until human QA verifies it.</p><div class="grid">{directory}</div></main>',1))
    for r in researchers:
        lane_html=""
        for key,label in [("discussion","Discussion"),("latex","LaTeX"),("presentation","Presentation")]:
            lane=r["lanes"][key]
            lane_html+=f'<article class="lane"><h3>{label}</h3><div class="code">{esc(lane["branch"])}</div><p class="muted">{esc(lane["content_policy"])}</p><a href="{branch_url(lane["branch"])}">Open Git branch →</a></article>'
        modules=[w for w in websites if w.get("researcher_id")==r["researcher_id"]]
        website_section=""
        if modules:
            module_cards=""
            for w in modules:
                wd=w.get("drive",{})
                extra=""
                if w.get("research_title"):
                    extra+=f'<p><strong>Research:</strong> {esc(w["research_title"])}</p>'
                if w.get("application_status"):
                    extra+=f'<p class="muted">Application: {esc(w["application_status"])}</p>'
                if w.get("research_status"):
                    extra+=f'<p class="muted">Research state: {esc(w["research_status"])}</p>'
                if wd.get("current_manuscript_pdf_id"):
                    extra+=f'<p><a href="{drive_url(wd["current_manuscript_pdf_id"])}">Open current manuscript PDF →</a></p>'
                if wd.get("submitted_form_e_pdf_id"):
                    extra+=f'<p><a href="{drive_url(wd["submitted_form_e_pdf_id"])}">Open submitted Form E →</a></p>'
                if w.get("public_site_path"):
                    live="https://fabingurung.github.io/JP_Research-and-Development"+w["public_site_path"]
                    extra+='<p><a href="'+esc(live)+'">Open published website →</a></p>'
                module_cards+='<article class="lane"><h3>'+esc(w["label"])+'</h3><div class="code">Researcher module · '+esc(w["state"])+'</div>'+extra+'<a href="'+branch_url(w["branch"])+'">Legacy branch (full repo snapshot) →</a></article>'
            website_section='<section class="section"><h2>Existing website modules</h2><div class="lanes">'+module_cards+'</div></section>'
        researcher_debts=[d for d in debts if d.get("researcher_id")==r["researcher_id"] and d.get("status") in ("OPEN","HOLD")]
        debt_section=""
        if researcher_debts:
            debt_section=f'<section class="section"><h2>Research debt</h2><div class="notice">{len(researcher_debts)} governed open/held item(s). <a href="debts/index.html">Open debt subpage →</a></div></section>'
        status_label="TITLE VERIFIED · OTHER POINTERS HOLD" if r["qa_status"]=="TITLE_VERIFIED_OTHER_POINTERS_HOLD" else "HOLD · HUMAN QA REQUIRED"
        title_value=r.get("topic_title") or "ON HOLD"
        notice_text=r.get("public_note") or ("Title verified by user; remaining Drive pointers stay on hold pending lane-specific QA." if r["qa_status"]=="TITLE_VERIFIED_OTHER_POINTERS_HOLD" else "Research topic, title, short page name and all Drive file IDs are intentionally unpublished until human QA.")
        drive=r["drive"]
        rows=[
          ("Discussion Google Doc",drive.get("discussion_google_doc_id")),
          ("Research project Drive folder",drive.get("project_root_drive_id")),
          ("Working thesis PDF",drive.get("working_pdf_drive_id")),
          ("LaTeX source",drive.get("latex_source_drive_id")),
          ("LaTeX source package",drive.get("latex_source_package_drive_id")),
          ("Formatting-only preview PDF (NON-PRODUCTION)",drive.get("preview_pdf_drive_id")),
          ("Formatting preview source ZIP",drive.get("preview_latex_source_package_drive_id")),
          ("Researcher review matrix",drive.get("discussion_review_matrix_drive_id")),
          ("Presentation PDF",drive.get("presentation_pdf_drive_id")),
          ("Presentation PPTX",drive.get("presentation_pptx_drive_id")),
          ("Word review derivative",drive.get("word_review_derivative_drive_id")),
          ("Working thesis DOCX",drive.get("working_thesis_docx_drive_id")),
          ("Unpromoted candidate DOCX",drive.get("candidate_source_docx_drive_id")),
          ("Scientific audit PDF",drive.get("science_audit_pdf_drive_id")),
          ("Researcher action PDF",drive.get("researcher_action_pdf_drive_id")),
          ("Discussion READ FIRST",drive.get("discussion_read_first_drive_id")),
          ("Live thesis Google Doc",drive.get("thesis_google_doc_id")),
          ("Live presentation Google Slides",drive.get("presentation_google_slides_drive_id")),
        ]
        links="".join(f'<div>{esc(label)}</div><div>{f"""<a href="{drive_url(fid)}">Open Drive file</a>""" if fid else """<span class="badge">ON HOLD</span>"""}</div>' for label,fid in rows)
        body=f'''<main class="wrap hero"><div class="eyebrow">{esc(r["researcher_id"])}</div><h1>{esc(r["display_name"])}</h1><p><span class="badge">{esc(status_label)}</span></p><div class="notice">{esc(notice_text)}</div><section class="section"><h2>Topic</h2><div class="kvs"><div>Title</div><div>{esc(title_value)}</div><div>Short name</div><div>{esc(r.get("topic_short_name") or "ON HOLD")}</div></div></section><section class="section"><h2>Version control and source</h2><p>Git branches are full-repository commits; these researcher-named refs are compatibility/work lanes. Public-safe website and tool code is versioned in the common <a href="https://github.com/FabinGurung/JP_Research-and-Development/tree/main">GitHub main repository</a>. Original thesis source packages and compiled outputs remain in Google Drive until an explicit source-code admission/migration is approved.</p></section><section class="section"><h2>Research lanes</h2><div class="lanes">{lane_html}</div></section>{website_section}{debt_section}<section class="section"><h2>Google Drive outputs</h2><div class="kvs">{links}</div></section></main>'''
        if drive.get("project_root_drive_id"):
            folder_url="https://drive.google.com/drive/folders/"+drive["project_root_drive_id"]
            body=body.replace("</main>",'<section class="section"><h2>Canonical project folder</h2><p><a href="'+esc(folder_url)+'">Open complete Google Drive project cabinet →</a></p><p>GitHub contains public-safe source and pointers; the Drive folder contains original/compiled researcher documents subject to Drive permissions.</p></section></main>')
        if r["slug"]=="safal-dawadi":
            body=body.replace("</main>",'<section class="section"><h2>LaTeX preparation control</h2><div class="notice">Researcher source, PDF and A9 states are independently versioned. Read live project controls and recent releases before claiming scientific, university-format or A9 Main approval.</div><p><a href="../../controls/latex/safal-dawadi/index.html">Open Safal project LaTeX status →</a></p></section></main>')
        # Folder-role aliases come from the provider-read registry, not inferred names.
        mapped=folder_by_slug[r["slug"]]
        present=[x for x in mapped["roles"] if x["existing_drive_folder_id"]]
        absent=[x for x in mapped["roles"] if not x["existing_drive_folder_id"]]
        role_items="".join(
            '<div>'+esc(x["logical_role"])+'</div><div><a href="'+esc("https://drive.google.com/drive/folders/"+x["existing_drive_folder_id"])+'">'+esc(x["current_name"])+'</a> · '+esc(x["status"])+'</div>'
            for x in present
        )
        unmapped="".join('<li>'+esc(x["logical_role"])+' — '+esc(x["status"])+'</li>' for x in absent)
        handover=REPO_URL+"/blob/main/docs/researcher-normalization/"+r["researcher_id"]+"__folder_handover.md"
        folder_section='<section class="section"><h2>Drive folder roles (ID-preserving)</h2>'
        folder_section+='<p>Role aliases are read-only, project ID is not asserted, and unchanged folders are REUSED. Local/Main acknowledgments are never inferred.</p>'
        folder_section+='<div class="kvs">'+role_items+'</div>'
        folder_section+='<details><summary>Unverified direct-child roles ('+str(len(absent))+')</summary><ul>'+unmapped+'</ul></details>'
        folder_section+='<p><a href="'+esc(handover)+'">Open owner-thread folder normalization handover →</a> · <a href="../../thesis-infrastructure/index.html">All researcher folder roles →</a></p></section>'
        body=body.replace("</main>",folder_section+"</main>")
        owner_prompt=REPO_URL+"/blob/main/prompts/researchers/"+r["researcher_id"]+"__"+r["slug"]+".md"
        owner_state=owner_by_id[r["researcher_id"]]["state"]
        owner_section='<section class="section"><h2>Opt-in workspace modernization</h2><p><strong>Execution state:</strong> '+esc(owner_state)+'</p>'
        owner_section+='<p>No folder changes occur unless the user pastes this exact owner-specific prompt in this researcher chat. Deletion is forbidden; safe reuse and evidence-backed archiving are preferred.</p>'
        owner_section+='<p><a href="'+esc(owner_prompt)+'">Open complete paste-ready owner prompt →</a></p></section>'
        body=body.replace("</main>",owner_section+"</main>")
        write(out,f'researchers/{r["slug"]}/index.html',shell(r["display_name"],body,2))
        if researcher_debts:
            debt_cards=""
            for d in researcher_debts:
                evidence=evidence_html(d)
                debt_cards+=f'<article class="card"><span class="badge">{esc(d["status"])}</span><h3>{esc(d["title"])}</h3><p>{esc(d["description"])}</p><p><strong>Category:</strong> {esc(d["category"])} · <strong>Severity:</strong> {esc(d["severity"])}</p><ul>{evidence}</ul><p><strong>Close when:</strong> {esc(d["close_when"])}</p></article>'
            debt_body=f'<main class="wrap hero"><div class="eyebrow">{esc(r["researcher_id"])} · governed debt</div><h1>{esc(r["display_name"])} — Research Debts</h1><p class="lead">Only verified open/held debt is listed here. Closing an item requires provider-read evidence and an updated registry state.</p><div class="grid">{debt_cards}</div><p><a href="../index.html">← Back to researcher workspace</a></p></main>'
            write(out,f'researchers/{r["slug"]}/debts/index.html',shell(f'{r["display_name"]} Debts',debt_body,3))
    folder_summary=[]
    for rr in folder_roles["records"]:
        root_id=rr.get("existing_project_root_drive_id")
        root_link='<a href="'+esc("https://drive.google.com/drive/folders/"+root_id)+'">Verified project root</a>' if root_id else '<strong>HOLD — root unknown</strong>'
        present=[x for x in rr["roles"] if x["existing_drive_folder_id"]]
        missing=[x for x in rr["roles"] if not x["existing_drive_folder_id"]]
        short=""
        for it in present:
            short+='<li><code>'+esc(it["logical_role"])+'</code> → <a href="'+esc("https://drive.google.com/drive/folders/"+it["existing_drive_folder_id"])+'">'+esc(it["current_name"])+'</a> · '+esc(it["status"])+'</li>'
        extras="".join('<li>'+esc(x["logical_role"])+": "+esc(x["current_name"])+'</li>' for x in rr["researcher_specific_extensions"])
        handover_link=REPO_URL+"/blob/main/docs/researcher-normalization/"+rr["researcher_id"]+"__folder_handover.md"
        prompt_link=REPO_URL+"/blob/main/prompts/researchers/"+rr["researcher_id"]+"__"+rr["researcher_slug"]+".md"
        migration_state=owner_by_id[rr["researcher_id"]]["state"]
        folder_summary.append('<article class="card"><h3>'+esc(rr["researcher_id"]+" · "+rr["researcher_slug"])+'</h3>'
            +'<p>'+root_link+' · '+str(len(present))+' roles mapped · '+str(len(missing))+' roles unverified as direct child</p>'
            +'<p><strong>Owner migration:</strong> '+esc(migration_state)+' · <strong>A9:</strong> '+esc(rr["a9_main_sync_status"])+'</p>'
            +'<details><summary>Show mapped folders and specialized paths</summary><ul>'+short+extras+'</ul></details>'
            +'<p><a href="'+esc(prompt_link)+'">Paste-ready execution prompt →</a> · <a href="'+esc(handover_link)+'">Folder audit →</a> · <a href="'+esc("../researchers/"+rr["researcher_slug"]+"/index.html")+'">Workspace →</a></p></article>')
    thesis_body='<main class="wrap hero"><div class="eyebrow">R&D · one thesis infrastructure</div><h1>Researcher Drive roles and document automation</h1>'
    thesis_body+='<p class="lead">Eleven registered researchers, ten verified project roots. Drive IDs are stable identity; folder aliases are human names. Reuse is preferred. Nothing here is a bulk folder move or scientific approval.</p>'
    thesis_body+='<div class="flow"><div class="node">A7 researcher ID</div><div class="arrow">→</div><div class="node">Drive folder ID</div><div class="arrow">→</div><div class="node">R&D shared code + one LaTeX tower</div><div class="arrow">→</div><div class="node">Owning project and A9 Local/Main</div></div>'
    thesis_body+='<section class="section"><h2>Governed reuse</h2><p>Drive: scientific sources, Google Docs, DOCX, Google Slides, Colab, artifacts and PDFs. Git: shared scripts, admitted manuscript sources, configuration, version history and QA metadata. The owner thread handles authorized physical changes only after A9 PRE/POST and readback.</p>'
    thesis_body+='<p><a href="'+esc(REPO_URL+"/blob/main/registry/researcher-folder-roles.json")+'">Folder role registry JSON →</a> · <a href="'+esc(REPO_URL+"/blob/main/controls/researcher-folder-contract.json")+'">Folder contract →</a> · <a href="'+esc(REPO_URL+"/blob/main/docs/THESIS_FOLDER_NORMALIZATION_GAP_MATRIX_20261009.md")+'">Gap matrix →</a></p></section>'
    thesis_body+='<section class="section"><h2>Researcher-chat activation</h2><p>Choose exactly one named prompt below and paste it into that researcher’s owning chat. The migration status is PENDING until that owner supplies verified provider PRE/POST evidence. Central GitHub does not move Drive data.</p><p><a href="'+esc(REPO_URL+"/tree/main/prompts/researchers")+'">Open all eleven individual owner prompts →</a> · <a href="'+esc(REPO_URL+"/blob/main/controls/researcher-migration-rules.json")+'">Read zero-delete governance →</a></p></section>'
    thesis_body+='<section class="section"><h2>Researcher workspace directory</h2><div class="grid">'+''.join(folder_summary)+'</div></section>'
    thesis_body+='<section class="section"><h2>Shared automation status</h2><p>PU v1.13 source inventory: 144/144 rule identifiers. Generic build profiles: 11/11. Source preflight and PDF technical inspector are available; full PU 144-rule rendered production compliance remains OPEN. GitHub source gates are not scientific PDF build gates.</p>'
    thesis_body+='<p><a href="'+esc(REPO_URL+"/blob/main/registry/latex-build-profiles.json")+'">Build profiles →</a> · <a href="'+esc(REPO_URL+"/blob/main/controls/latex/pu-rule-enforcement-matrix.json")+'">144-rule enforcement roadmap →</a> · <a href="' + esc(REPO_URL+"/blob/main/docs/UNIVERSAL_THESIS_BUILD_READ_FIRST_20261009.md") + '">Linux build procedure →</a> · <a href="../controls/latex/index.html">Single LaTeX tower →</a></p></section></main>'
    write(out,"thesis-infrastructure/index.html",shell("Thesis Infrastructure",thesis_body,1))
    # Unified R&D main codebase: Fabin research subpages are deployed together.
    sitebase="https://fabingurung.github.io/JP_Research-and-Development"
    fabin=next(r for r in researchers if r["slug"]=="fabin-gurung")
    fdrive=fabin["drive"]
    aec_research=[
        ("Current MSc Structural thesis working PDF",drive_url(fdrive.get("working_pdf_drive_id"))),
        ("LaTeX source ZIP (Git source transition pending)",drive_url(fdrive.get("latex_source_package_drive_id"))),
        ("Midterm presentation PPTX",drive_url(fdrive.get("presentation_pptx_drive_id"))),
        ("Midterm presentation QA PDF",drive_url(fdrive.get("presentation_pdf_drive_id"))),
        ("Canonical Drive project cabinet","https://drive.google.com/drive/folders/"+fdrive["project_root_drive_id"]),
        ("Static AEC methodology demo",sitebase+"/methodology-demo/"),
        ("JP Structural Analysis engine","https://fabingurung.github.io/JP_Structural_Analysis/"),
        ("Current GitHub source repository","https://github.com/FabinGurung/JP_Research-and-Development/tree/main")
    ]
    def cards_for(links):
        return "".join('<article class="card"><h3>'+esc(label)+'</h3><a href="'+esc(url)+'">Open →</a></article>' for label,url in links if url)
    aec_body='<main class="wrap hero"><div class="eyebrow">Fabin Gurung / Paper 01 · MSc Structural Engineering</div><h1>'+esc(fabin["topic_title"])+'</h1><p class="lead">The AEC research website and original interactive methodology demo are now accessible within the unified JP R&D Pages build. v0.9 thesis is a QA-passed WORKING document, not a certified final submission.</p><div class="grid">'+cards_for(aec_research)+'</div><section class="section"><h2>Code and provenance</h2><p>Live portal code is on repository <strong>main</strong>. Restored standalone demos are under <code>web/legacy-site/methodology-demo</code>, retaining the archived public-source blob identities. Git branches are whole-repository snapshots, not one-researcher file stores. Original research documents remain in Drive.</p><p><a href="../../index.html">← Fabin researcher workspace</a></p></section></main>'
    write(out,"researchers/fabin-gurung/websites/aec/index.html",shell("Fabin AEC Research",aec_body,4))
    hydro=next(w for w in websites if w.get("module_slug")=="hydropower-phd")
    hd=hydro.get("drive",{})
    proposal=hydro["proposal_defense_source"]
    hydro_links=[
        ("Current post-defense manuscript PDF (non-final)",drive_url(hd.get("current_manuscript_pdf_id"))),
        ("Current LaTeX manuscript source ZIP",drive_url(hd.get("current_manuscript_source_zip_id"))),
        ("Submitted PhD Form E PDF",drive_url(hd.get("submitted_form_e_pdf_id"))),
        ("PhD application cabinet","https://drive.google.com/drive/folders/"+hd["phd_application_root_id"]),
        ("Post-defense working research folder","https://drive.google.com/drive/folders/"+hd["post_defense_revision_root_id"]),
        ("Proposal defense viewer",sitebase+"/researchers/fabin-gurung/websites/hydropower-phd/proposal-defense/"),
        ("Nepal hydropower research map · archived demo",sitebase+"/hydropower-nepal-map/"),
        ("Relational model · schema view",sitebase+"/hydropower-data-schema/"),
        ("Relational model · table designer",sitebase+"/hydropower-data-tables/"),
        ("Relational model · interactive graph",sitebase+"/hydropower-data-graph/"),
        ("GitHub research site source","https://github.com/FabinGurung/JP_Research-and-Development/tree/main")
    ]
    hydro_body='<main class="wrap hero"><div class="eyebrow">Fabin Gurung / Paper 02 · Hydropower PhD research</div><h1>'+esc(hydro["research_title"])+'</h1><p class="lead">Post-defense research framework: BIM/GIS, hydropower assets and normalized relationships for traceable infrastructure planning. Current manuscript v0.2 is QA-pass review, NOT a final PhD submission. Historical static visualizations are restored as research demos; they are not new verified site-suitability evidence.</p><div class="grid">'+cards_for(hydro_links)+'</div><section class="section"><h2>Scientific boundaries</h2><p>M1–M3 are not a final all-module scientific freeze, M4 remains unselected and M5 acceptance cutoffs remain open. Prototype GIS research and hydropower research-model demos do not replace formal feasibility, surveys or licensed engineering analysis.</p><p><a href="../../index.html">← Fabin researcher workspace</a></p></section></main>'
    write(out,"researchers/fabin-gurung/websites/hydropower-phd/index.html",shell("Fabin Hydropower PhD",hydro_body,4))
    defense_pdf=drive_url(proposal["pdf_seq16_drive_id"])
    defense_pptx=drive_url(proposal["pptx_seq16_drive_id"])
    defense_body='<main class="wrap hero"><div class="eyebrow">Fabin Gurung · PhD proposal defense · governed Drive output</div><h1>Hydropower research proposal defense</h1><p class="lead">Published GitHub page, provider-hosted PDF. This SEQ16 file is a historical proposal-defense output and is not a final defense/submission certificate.</p><p><a href="'+defense_pdf+'">Open proposal-defense PDF in Google Drive →</a> · <a href="'+defense_pptx+'">Open editable PPTX →</a></p><div style="height:70vh;min-height:450px"><iframe title="PhD proposal-defense PDF" style="width:100%;height:100%;border:1px solid #ccd;border-radius:10px" loading="lazy" src="https://drive.google.com/file/d/'+esc(proposal["pdf_seq16_drive_id"])+'/preview"></iframe></div><p>Google Drive permissions or browser privacy settings may block embedded preview; use the direct link above.</p><p><a href="../index.html">← Hydropower research page</a></p></main>'
    write(out,"researchers/fabin-gurung/websites/hydropower-phd/proposal-defense/index.html",shell("Hydropower Proposal Defense",defense_body,5))
    # Compatibility URLs preserve the legacy demo navigation without running old Next.js code.
    for old_path,label,target in (
        ("aec/index.html","AEC research",sitebase+"/researchers/fabin-gurung/websites/aec/"),
        ("hydropower/index.html","Hydropower PhD research",sitebase+"/researchers/fabin-gurung/websites/hydropower-phd/"),
        ("hydropower/proposal-defense/index.html","Hydropower proposal defense",sitebase+"/researchers/fabin-gurung/websites/hydropower-phd/proposal-defense/"),
    ):
        alias_body='<main class="wrap hero"><div class="eyebrow">Preserved legacy website route</div><h1>'+esc(label)+'</h1><p class="lead">The GitHub source site now has a new unified researcher subpage. The original research demo assets remain preserved and directly navigable.</p><p><a href="'+esc(target)+'">Open current research subpage →</a></p></main>'
        write(out,old_path,shell("Legacy route to "+label,alias_body,old_path.count("/")))
    manoj_debts=[d for d in debts if d.get("audit_slug")=="manoj-bhandari" and d.get("status") in ("OPEN","HOLD")]
    audit_root="audits/02-thesis/manoj-bhandari/"
    manoj_certificate=manoj_audit["verified_certificate"]
    audit_links=f'<a href="{drive_url(manoj_certificate["stable_current_pdf_drive_id"])}">Open current certificate PDF →</a>'
    audit_summary=f'<main class="wrap hero"><div class="eyebrow">Direct-child Drive audit · certificate only</div><h1>Manoj Bhandari</h1><p class="lead">Verified certificate authority: {esc(manoj_certificate["title_from_certificate_not_separately_verified_thesis_current"])}</p><p>{esc(manoj_certificate["state"])}</p><div class="notice">No independently verified active thesis workspace was found in the audited child. A certificate alone does not authorize a researcher lane or site.</div><p>{audit_links}</p><p><a href="debts/index.html">Review Manoj authority hold →</a></p></main>'
    write(out,audit_root+"index.html",shell("Manoj Bhandari Audit",audit_summary,3))
    manoj_cards="".join(f'<article class="card"><span class="badge">{esc(d["status"])}</span><h3>{esc(d["title"])}</h3><p>{esc(d["description"])}</p><ul>{evidence_html(d)}</ul><p><strong>Close when:</strong> {esc(d["close_when"])}</p></article>' for d in manoj_debts)
    manoj_body=f'<main class="wrap hero"><div class="eyebrow">Direct-child audit · governed hold</div><h1>Manoj Bhandari — Authority Debts</h1><p class="lead">This is not an active researcher workspace. No thesis source, Discussion, Presentation or website may be invented.</p><div class="grid">{manoj_cards}</div><p><a href="../index.html">← Back to Manoj audit</a></p></main>'
    write(out,audit_root+"debts/index.html",shell("Manoj Bhandari Debts",manoj_body,4))
    avishek_debts=[d for d in debts if d.get("audit_slug")=="avishek-kumar-mandal" and d.get("status") in ("OPEN","HOLD")]
    avishek_root="audits/02-thesis/avishek-kumar-mandal/"
    draft=avishek_audit["verified_source"]
    avishek_body=f'<main class="wrap hero"><div class="eyebrow">Direct-child Drive audit · first-draft intake</div><h1>Avishek Kumar Mandal</h1><p class="lead">{esc(draft["title_from_user_uploaded_draft"])}</p><div class="notice">One preserved first draft, not an approved current thesis. Reported Prism LaTeX/PDF are unavailable and were not promoted. No active researcher branch created.</div><p><a href="{drive_url(draft["draft_docx_drive_id"])}">Open original first-draft DOCX →</a></p><p><a href="debts/index.html">Open authority and methodology holds →</a></p></main>'
    write(out,avishek_root+"index.html",shell("Avishek Kumar Mandal Audit",avishek_body,3))
    avishek_cards="".join(f'<article class="card"><span class="badge">{esc(d["status"])}</span><h3>{esc(d["title"])}</h3><p>{esc(d["description"])}</p><ul>{evidence_html(d)}</ul><p><strong>Close when:</strong> {esc(d["close_when"])}</p></article>' for d in avishek_debts)
    avishek_debt_body=f'<main class="wrap hero"><div class="eyebrow">Direct-child audit · governed holds</div><h1>Avishek Kumar Mandal — Authority Debts</h1><div class="grid">{avishek_cards}</div><p><a href="../index.html">← Back to Avishek audit</a></p></main>'
    write(out,avishek_root+"debts/index.html",shell("Avishek Authority Debts",avishek_debt_body,4))
    inventory_rows="".join(f'<tr><td>{row["position"]}</td><td>{esc(row["name"])}</td><td class="code">{esc(row["drive_id"])}</td></tr>' for row in root_rescan["children"])
    extra=root_rescan["newly_observed_vs_previous_inventory"]
    extra_text=", ".join(x["name"] for x in extra) or "None"
    root_body=f'<main class="wrap hero"><div class="eyebrow">02_Thesis · direct-child rescan</div><h1>Drive folder inventory</h1><p class="lead">{root_rescan["current_inventory_count"]} direct children. Newly observed vs previous inventory: {esc(extra_text)}. An inventory addition does not prove a new creation date.</p><section class="section"><h2>Provider order</h2><table><thead><tr><th>#</th><th>Folder</th><th>Drive ID</th></tr></thead><tbody>{inventory_rows}</tbody></table></section><p><a href="manoj-bhandari/index.html">Manoj audit</a> · <a href="avishek-kumar-mandal/index.html">Avishek audit</a></p></main>'
    write(out,"audits/02-thesis/index.html",shell("02 Thesis Inventory",root_body,2))
    # Independent direct-child audit surfaces; these do not create researcher branches.
    audited_names={
        "rural-road-maintenance":"Rural Road Maintenance",
        "safal-dawadi":"Safal Dawadi",
        "saugat-paneru":"Saugat Paneru",
        "nabin-bista":"Nabin Bista",
        "krishna-kumar-gupta":"Krishna Kumar Gupta",
        "shisheer-kc":"Shisheer KC",
        "sunil-rana":"Sunil Rana",
        "fabin-gurung":"Fabin Gurung",
        "master-index":"00 Master Index"
    }
    source_showcase={
        "rural-road-maintenance":("Preferred archived proposal deck","1F-BfaUV5DcHTIO240npPVYuRUNgnaYDc"),
        "safal-dawadi":("v1.9 controlled qualitative review PDF","1R9lRxDfgrvB1-s-o4-Y7GuN56zeD5itb"),
        "saugat-paneru":("CP114 exact-TNR production manuscript","1aFVnwamHhp2Xpjmg10UfMPBwK031HMTh"),
        "nabin-bista":("Current Google Docs manuscript","1v5QKdtwFVmvl5QVhq1jaWSdKfXj1YidGxNzzpKVu-hU"),
        "krishna-kumar-gupta":("v0.3.5 working thesis PDF","1zHKtBKkCIDG_fGQvFCLzmLHP7uzJ25x0"),
        "shisheer-kc":("CKPT14 controlled baseline","1ZjOECL8NKfRKBfcyeyiERN1HEZTK_5_r"),
        "sunil-rana":("Working v0.1 DOCX","1beFNMsWUkMXS-OTnvt1x0Uiud1N4okGg"),
        "fabin-gurung":("v0.9 working MSc Structural thesis","1LBt3R4u35BxhKjOGoX8YflP7zFJutxBk"),
        "master-index":("Thesis-wide control tower","1jc6WIqXbAixAYYndeB2Idw59fAzjBbnDKlq49THeu_A")
    }
    for slug,audit in batch_audits.items():
        display=audited_names[slug]
        title=audit.get("title") or audit.get("title_from_current_pdf") or audit.get("title_from_historical_proposal") or "Unverified title"
        status=audit.get("classification","AUDITED")
        items=audit.get("unresolved",[])
        debt_rows=[d for d in debts if d.get("audit_slug")==slug or d.get("researcher_id")==audit.get("researcher_id") and audit.get("researcher_id")]
        count=len(debt_rows)
        label,source_id=source_showcase[slug]
        warning='<div class="notice">This is a provider-grounded classification, not approval to alter a scientific manuscript, enroll a researcher, or release a submission.</div>'
        open_items="".join(f'<li>{esc(x)}</li>' for x in items)
        root=f"audits/02-thesis/{slug}/"
        body=f'<main class="wrap hero"><div class="eyebrow">Drive audit · {esc(audit["direct_child"])}</div><h1>{esc(display)}</h1><p class="lead">{esc(title)}</p><p><span class="badge">{esc(status)}</span></p>{warning}<section class="section"><h2>Verified source</h2><p><a href="{drive_url(source_id)}">{esc(label)} →</a></p><p><a href="https://drive.google.com/drive/folders/{esc(audit["root_folder_id"])}">Open original Drive folder →</a></p></section><section class="section"><h2>Open boundaries</h2><ul>{open_items}</ul></section><p><a href="debts/index.html">{count} associated debt item(s) — open debt subpage →</a></p></main>'
        write(out,root+"index.html",shell(f"{display} Audit",body,3))
        cards="".join(f'<article class="card"><span class="badge">{esc(d["status"])}</span><h3>{esc(d["debt_id"])} — {esc(d["title"])}</h3><p>{esc(d["description"])}</p><ul>{evidence_html(d)}</ul><p><strong>Close when:</strong> {esc(d["close_when"])}</p></article>' for d in debt_rows)
        db=f'<main class="wrap hero"><div class="eyebrow">Direct-child audit · governed debt register</div><h1>{esc(display)} — Research Debts</h1><p class="lead">Scientific and administrative holds are explicit. This page does not authorize resuming protected work.</p><div class="grid">{cards}</div><p><a href="../index.html">← Back to {esc(display)} audit</a></p></main>'
        write(out,root+"debts/index.html",shell(f"{display} Debts",db,4))
    active_debt_cards=""
    resolved_debt_cards=""
    for d in debts:
        owner=f' · {esc(d.get("researcher_slug") or d.get("audit_slug"))}' if d.get("researcher_slug") or d.get("audit_slug") else ""
        detail=""
        if d.get("audit_slug") in ("manoj-bhandari","avishek-kumar-mandal",*batch_audits.keys()):
            detail=f'<p><a href="../audits/02-thesis/{esc(d["audit_slug"])}/debts/index.html">Open direct-child audit debt subpage →</a></p>'
        elif d.get("researcher_slug"):
            detail=f'<p><a href="../researchers/{esc(d["researcher_slug"])}/debts/index.html">Open researcher debt subpage →</a></p>'
        card=f'<article class="card"><span class="badge">{esc(d["status"])}</span><h3>{esc(d["debt_id"])}{owner}</h3><h3>{esc(d["title"])}</h3><p>{esc(d["description"])}</p><ul>{evidence_html(d)}</ul><p><strong>Close when:</strong> {esc(d["close_when"])}</p>{detail if d["status"]!="CLOSED" else ""}</article>'
        if d["status"]=="CLOSED": resolved_debt_cards+=card
        else: active_debt_cards+=card
    debt_page=f'<main class="wrap hero"><div class="eyebrow">Research debt / holds</div><h1>Open debts and governed holds</h1><p class="lead">Only OPEN/HOLD items require action. HOLD items are not permission to resume them.</p><div class="grid">{active_debt_cards}</div><section class="section"><h2>Resolved readbacks and closed items</h2><div class="grid">{resolved_debt_cards}</div></section></main>'
    write(out,"debts/index.html",shell("Research Debts",debt_page,1))
    workspace=f'''<main class="wrap hero"><div class="eyebrow">Repository field</div><h1>Workspace</h1><p class="lead">This repository is a code-and-pointer control plane for R&D. It is not the document warehouse.</p><section class="section"><div class="kvs"><div>Main</div><div>Portal code, shared controls, researcher registry, schemas, Drive/GitHub pointers.</div><div>Discussion lane</div><div>Google Doc ID/link and automation metadata only; discussion prose remains in Drive.</div><div>LaTeX lane</div><div>.tex/.bib/build code; compiled PDF is uploaded to Drive.</div><div>Presentation lane</div><div>TypeScript/PptxGenJS/YAML/JSON/HTML/CSS/SVG; generated PPTX/PDF is uploaded to Drive.</div><div>Archive</div><div>Git history plus legacy branches classified read-only.</div></div></section><section class="section"><h2>Branch state</h2><p>{len(branches["archived_legacy"])} legacy refs are archived under <strong>archive/</strong>. The model defines {len(branches["active_researcher_lanes"])} legacy-compatible full-repository branch refs (researcher folders and current code share main) plus {len(branches.get("active_website_modules",[]))} verified optional website lanes.</p></section></main>'''
    workspace=workspace.replace("</main>",'<section class="section"><h2>Additional audited Drive children</h2><p><a href="../audits/02-thesis/index.html">02_Thesis — rescan inventory (18 direct children) →</a></p><p><a href="../audits/02-thesis/manoj-bhandari/index.html">Manoj Bhandari — certificate-only audit →</a></p><p><a href="../audits/02-thesis/avishek-kumar-mandal/index.html">Avishek Kumar Mandal — first-draft intake audit →</a></p><p><a href="../audits/02-thesis/rural-road-maintenance/index.html">Rural Road Maintenance — archive-intake audit →</a></p><p><a href="../audits/02-thesis/safal-dawadi/index.html">Safal Dawadi — CM thesis audit →</a></p><p><a href="../audits/02-thesis/saugat-paneru/index.html">Saugat Paneru — CP114 audit →</a></p><p><a href="../audits/02-thesis/nabin-bista/index.html">Nabin Bista — live Docs audit →</a></p><p><a href="../audits/02-thesis/krishna-kumar-gupta/index.html">Krishna Kumar Gupta — v0.3.5 audit →</a></p><p><a href="../audits/02-thesis/shisheer-kc/index.html">Shisheer KC — CKPT14 baseline and CKPT15 candidate →</a></p><p><a href="../audits/02-thesis/sunil-rana/index.html">Sunil Rana — scientific review →</a></p><p><a href="../audits/02-thesis/fabin-gurung/index.html">Fabin Gurung — v0.9 AEC manuscript →</a></p><p><a href="../audits/02-thesis/master-index/index.html">00 Master Index — shared thesis infrastructure →</a></p></section></main>')
    write(out,"workspace/index.html",shell("Workspace",workspace,1))
    cards=""
    for name,c in controls.items():
        slug=name.lower().replace("latex","latex")
        cards+=f'<article class="card"><h3>{name}</h3><p>Control ID: <span class="code">{esc(c["control_id"])}</span></p><a href="{slug}/index.html">Open control →</a></article>'
    write(out,"controls/index.html",shell("Controls",f'<main class="wrap hero"><div class="eyebrow">Shared control towers</div><h1>One format for every researcher</h1><p class="lead">Researcher lanes inherit these contracts so ChatGPT does not invent a new workflow per researcher.</p><div class="controls">{cards}</div></main>',1))
    for name,c in controls.items():
        slug=name.lower()
        body=f'<main class="wrap hero"><div class="eyebrow">Shared control</div><h1>{name}</h1><div class="kvs"><div>Control ID</div><div class="code">{esc(c["control_id"])}</div><div>Status</div><div>{esc(c["status"])}</div><div>Branch pattern</div><div class="code">{esc(c.get("branch_pattern","researcher/<slug>/latex"))}</div><div>Authority</div><div>{esc(c.get("authority",c.get("authority_path","MODULE_AUTHORITY")))}</div></div><section class="section"><h2>Workflow</h2><ol>'+''.join(f'<li>{esc(x)}</li>' for x in c.get("workflow",c.get("change_flow",[])))+'</ol></section></main>'
        if slug=="latex":
            fmt=load(Path("controls/latex/format-authorities.json"))
            rule=load(Path("controls/latex/pu-msc-format.rules.json"))
            migration=load(Path("controls/latex/migration-status.json"))
            bcontract=load(Path("controls/latex/build-contract.json"))
            qcontract=load(Path("controls/latex/qa-contract.json"))
            rcontract=load(Path("controls/latex/release-contract.json"))
            basegit=REPO_URL+"/blob/main/controls/latex/"
            contract_links="".join('<li><a href="'+esc(basegit+p)+'">'+esc(p)+' →</a></li>' for p in ("README.md","format-authorities.json","pu-msc-format.rules.json","build-contract.json","qa-contract.json","release-contract.json","migration-status.json"))
            steps="".join('<div class="node">'+esc(s.replace("_"," ").title())+'</div>'+('<div class="arrow">→</div>' if i<len(bcontract["build_stages"])-1 else "") for i,s in enumerate(bcontract["build_stages"]))
            fmtitems="".join('<li>'+esc(str(x["key"]).replace("_"," ").title())+': <strong>'+esc(x["value"])+'</strong> · '+esc(x["verification"])+'</li>' for x in rule["obligations"])
            qaitems="".join('<li>'+esc(x)+'</li>' for x in qcontract["whole_document_render"])
            repo_name="FabinGurung/JP_Research-and-Development"
            sourceitems="".join('<li><a href="'+esc(x.get("url") or "https://github.com/"+x.get("repository",repo_name)+"/blob/main/"+x.get("path",""))+'">'+esc(x["role"])+' — '+esc(x.get("observed_version",x.get("observed_version","R&D executable")))+ '</a> · '+esc(x["status"])+'</li>' for x in fmt["sources"])
            bridge='<section class="section"><h2>Control inheritance</h2><div class="flow">'+steps+'</div><p>A7 global bootstrap → R&D module and shared LaTeX control → project configuration → admitted manuscript → build and independent QA → Google Drive readback → separately governed A9 registration.</p></section>'
            bridge+='<section class="section"><h2>Original authorities and provenance</h2><ul>'+sourceitems+'</ul><p class="notice">Original Drive formatting and scientific controls continue to govern unresolved rules; machine bridge is not a full university-format certification.</p></section>'
            bridge+='<section class="section"><h2>Format selection</h2><p>'+esc(rule["discovered_unique_rule_ids"])+' distinct PU rule identifiers indexed; '+esc(migration["format_rule_ids_interpreted"])+' selected interpretations; the remaining original obligations are not yet automated.</p><ul>'+fmtitems+'</ul></section>'
            bridge+='<section class="section"><h2>Build and QA gates</h2><p>XeLaTeX → Biber → XeLaTeX → XeLaTeX. A successful code gate is not a thesis compile, visual approval, scientific approval or Drive publication.</p><ul>'+qaitems+'</ul></section>'
            central=load(Path("controls/latex/tower.json"))
            inheritance=load(Path("registry/latex-inheritance.json"))
            amendments=load(Path("controls/latex/change-register.json"))
            researcher_entries="".join('<li><a href="'+esc(REPO_URL+"/blob/main/registry/latex-inheritance.json")+'">'+esc(x["researcher_id"]+" / "+x["slug"])+'</a> — shared base '+esc(x["template"])+'; '+esc(x["configuration_status"])+'</li>' for x in inheritance["researchers"])
            bridge+='<section class="section"><h2>One template for every researcher</h2><p><strong>ONE SOURCE OF TRUTH:</strong> <a href="'+esc(REPO_URL+"/blob/main/controls/latex/tower.json")+'">canonical tower.json</a> and <a href="'+esc(REPO_URL+"/blob/main/controls/latex/template/pumlsc-shared.sty")+'">one shared LaTeX .sty template</a>. No person has a fork of this baseline. A7 is routing only.</p><p>'+str(len(inheritance["researchers"]))+' researchers inherit this shared template; personal manuscript metadata and explicit additions are parameters, not rival control towers.</p><details><summary>Every researcher and inherited source</summary><ul>'+researcher_entries+'</ul></details></section>'
            bridge+='<section class="section"><h2>Safal LaTeX chat handover and runnable Linux preview</h2><p><a href="'+esc(REPO_URL+"/blob/main/docs/HANDOVER_SAFAL_DAWADI_LATEX_EXECUTION_20261009.md")+'">Open full governed execution/handover for Safal v1.9 →</a></p><p>Infrastructure CI is stable, but <strong>the latest reconciled seq15 manuscript source is not yet in Git</strong>. After byte-verified source admission, the shared build script supports <code>check</code>, <code>preview</code> (explicit non-production Tinos), and <code>compile</code> (licensed Times New Roman only). No full PU parity or scientific approval is implied.</p></section>'
            bridge+='<section class="section"><h2>Shared fixes and numbered local amendments</h2><p>Common rules occupy the 001–100 namespace only as implemented; new tracked proposals start at <strong>101</strong>. A formatting improvement from any thesis must enter the <a href="'+esc(REPO_URL+"/blob/main/controls/latex/change-register.json")+'">one central amendment ledger</a> and is either promoted into the shared .sty after regression QA or logged as a justified researcher-only extension. Local exceptions never duplicate the core.</p><p>Next unallocated ID: '+esc(amendments["next_number"])+'; current recorded amendments: '+str(len(amendments["entries"]))+'. <a href="'+esc(REPO_URL+"/blob/main/controls/latex/extension-registry.json")+'">Project extension index →</a></p></section>'
            parity=load(Path("controls/latex/pu-format-parity-audit.json"))
            par_rows="".join('<tr><td>'+esc(x["id"])+'</td><td>'+esc(x["title"])+'</td><td>'+esc(x["parity_status"])+'</td><td>'+esc(x["evidence_note"])+'</td></tr>' for x in parity["per_rule"])
            summary=parity["counts"]
            bridge+='<section class="section"><h2>Full PU formatting source-parity audit</h2><p><strong>144 / 144 approved Drive v1.13 source rule IDs mapped.</strong> The original has no PU-FMT-076. Implementation status: '+str(summary["source_declared"])+' source-declared but not PDF verified; '+str(summary["partial_or_policy"])+' partial/policy; '+str(summary["missing_or_unverified"])+' not implemented or unverified. <strong>Zero production-approved PDF format tests</strong> (not a certification).</p><p><a href="'+esc(REPO_URL+"/blob/main/controls/latex/pu-format-parity-audit.json")+'">Inspect each rule and audit evidence in GitHub →</a></p><details><summary>All 144 rules and outstanding parity disposition</summary><div class="code" style="overflow-x:auto"><table style="width:100%;border-collapse:collapse"><thead><tr><th>PU rule</th><th>Subject</th><th>Evidence status</th><th>Explanation</th></tr></thead><tbody>'+par_rows+'</tbody></table></div></details></section>'
            bridge+='<section class="section"><h2>Approved Q1B / Q2A / Q3A</h2><p><strong>Q1:</strong> Safal latest Local seq15 v1.9 42-page source/PDF is the selected target; reconstructed ZIP/PDF bytes and the same-ID Drive replacement remain to be verified. The older v1.2 Midterm and first-upload v1.9 cannot substitute for it.</p><p><strong>Q2:</strong> PRE = earlier Git commit, POST = new non-force commit. Major accepted releases receive annotated Git tags once tag-write is supported; <strong>no routine new snapshot branches</strong>. All historical refs remain preserved.</p><p><strong>Q3:</strong> Admitted academic LaTeX manuscript source (.tex, .bib) belongs under each researcher in this R&D Git repository. Produce normal, evidence-grounded academic writing without internal AI/workflow QA narration or fabricated research.</p><p><a href="'+esc(REPO_URL+"/blob/main/docs/LATEX_Q1B_Q2A_Q3A_GOVERNED_CHANGE_20261009.md")+'">Read source change register →</a></p></section>'
            bridge+='<section class="section"><h2>Release and migration status</h2><p><strong>Bridge:</strong> '+esc(migration["status"])+'</p><p><strong>Cutover:</strong> '+esc(migration["cutover"])+'</p><p><strong>Source states:</strong> '+esc(", ".join(rcontract["states"]))+'</p><p><a href="safal-dawadi/index.html">Safal Dawadi control and release gate →</a> · <a href="../../researchers/safal-dawadi/latex/index.html">Safal researcher workspace →</a></p><h3>Source files</h3><ul>'+contract_links+'</ul></section>'
            body=body.replace("</main>",bridge+"</main>")
        write(out,f"controls/{slug}/index.html",shell(name,body,2))
    saf=load(Path("controls/projects/safal-dawadi.latex.json"))
    pub=saf["source_states"]["first_drive"]
    lane_items="".join('<li><a href="'+branch_url(v)+'">'+esc(k.title())+' branch →</a> '+esc(v)+'</li>' for k,v in saf["branches"].items() if k in ("discussion","latex","presentation"))
    gate_rows="".join('<div>'+esc(k.replace("_"," ").title())+'</div><div><span class="badge">'+esc(v)+'</span></div>' for k,v in saf["gates"].items())
    safal_body='<main class="wrap hero"><div class="eyebrow">RSH-010 · Project-specific LaTeX build authority</div><h1>Safal Dawadi — LaTeX control</h1><p class="lead">A7 routes; R&D owns reusable build controls; Drive retains approved PU formatting, scientific evidence and compiled PDFs.</p><div class="notice">CONTROL PREPARED, SOURCE NOT ADMITTED. Two v1.9 byte states differ; no release, PDF compile or Main Library ACK has been performed.</div><section class="section"><h2>Existing three functional branches</h2><ul>'+lane_items+'</ul><p>The branches are old template refs, not his imported manuscript.</p></section><section class="section"><h2>Drive v1.9 review candidate</h2><div class="kvs"><div>Published source ZIP</div><div><a href="'+drive_url(pub["source_zip"])+'">Open Drive ZIP →</a></div><div>42-page review PDF</div><div><a href="'+drive_url(pub["pdf"])+'">Open Drive PDF →</a></div><div>Later local reconciled build</div><div><span class="badge">HOLD · not mirrored</span></div><div>A9 Library</div><div>Local seq15 reported; Main ACK cursor5 held</div></div></section><section class="section"><h2>Release gates</h2><div class="kvs">'+gate_rows+'</div></section><section class="section"><h2>R&D control source</h2><p><a href="https://github.com/FabinGurung/JP_Research-and-Development/tree/resource/control/latex/v004-20261009">Shared LaTeX control release v004 (whole repository snapshot) →</a></p><p><a href="https://github.com/FabinGurung/JP_Research-and-Development/blob/main/controls/latex.control.json">Shared LaTeX rules →</a> · <a href="https://github.com/FabinGurung/JP_Research-and-Development/blob/main/controls/projects/safal-dawadi.latex.json">Safal control machine JSON →</a> · <a href="https://github.com/FabinGurung/JP_Research-and-Development/blob/main/docs/LATEX_CONTROL_OWNERSHIP.md">Source and ownership runbook →</a></p></section><section class="section"><h2>Original authoritative controls</h2><p><a href="https://docs.google.com/document/d/'+esc(saf["original_drive"]["pu_format"])+'/edit">PU formatting v1.13 →</a> · <a href="https://docs.google.com/document/d/'+esc(saf["original_drive"]["thesis_control"])+'/edit">Thesis control v1.23 →</a></p></section></main>'

    current=saf["current_source_manifest_candidate"]
    oct_observ='<section class="section"><h2>Current source-manifest Midterm candidate</h2><p>October 2026 <strong>v1.2 Midterm</strong> — controlled 28-page preview, not production. Times New Roman remains unavailable and Tinos fallback was used. These files are Drive candidates, not admitted Git source.</p><ul><li><a href="'+esc(drive_url(current["source_zip_id"]))+'">Manifest-designated v1.2 source ZIP →</a></li><li><a href="'+esc(drive_url(current["pdf_id"]))+'">Manifest-designated v1.2 preview PDF →</a></li></ul><p>The separately updated v1.9 42-page review is a pending Local seq15 lineage; its superiority or approval cannot be inferred from its higher number. Local reports Main cursor5; the independent Main registry row read still shows the older seq2 closeout, so seq15 Main ACK is not verified.</p></section>'
    safal_body=safal_body.replace("</main>",oct_observ+"</main>")
    # Historic Safal control URL retained for compatibility; no second tower page.
    safal_body='<main class="wrap hero"><h1>Safal LaTeX project configuration</h1><p>There is one shared R&D LaTeX control tower and one base template. Safal owns only project metadata, scientific evidence and any centrally registered extensions.</p><p><a href="../index.html">Open the single canonical LaTeX control tower →</a></p><p><a href="../../../researchers/safal-dawadi/latex/index.html">Open Safal project status and configuration →</a></p></main>'
    write(out,"controls/latex/safal-dawadi/index.html",shell("Safal Project Configuration",safal_body,3))
    scoped=load(Path("researchers/safal-dawadi/latex/control.json"))
    baseline=load(Path("researchers/safal-dawadi/latex/source-baseline.json"))
    research_body='<main class="wrap hero"><div class="eyebrow">Researcher / RSH-010 / configuration inherits single shared LaTeX</div><h1>Safal Dawadi — source governance</h1><p class="lead">Project-specific control inherits the reusable R&D operational tower; the approved Drive project remains the source for science and PU formatting.</p><div class="notice">SELECTED TARGET: Safal v1.9 Local seq15, 42-page reconciled build. Same-ID Drive mirror/hash is pending, so manuscript source is not yet imported and no new production PDF or A9 ACK is claimed.</div><section class="section"><h2>Active configuration</h2><div class="kvs"><div>Researcher</div><div>'+esc(scoped["researcher_id"])+'</div><div>Citation style</div><div>'+esc(scoped["citation_style"])+'</div><div>Stage</div><div>'+esc(scoped["document_stage"])+' — verify in Drive</div><div>Source admission</div><div>'+esc(scoped["source_admission"])+'</div><div>First upload hash (not selected)</div><div class="code">'+esc(baseline["first_drive_published"]["source_sha256_reported"])+' (older first v1.9 build)</div><div>Local candidate</div><div>'+esc(baseline["later_local_reported"]["drive_publication"])+'</div><div>A9 Local/Main</div><div>seq15 reported; Main cursor5 held</div></div></section><section class="section"><h2>Provider and source links</h2><ul><li><a href="'+esc(REPO_URL+'/blob/main/researchers/safal-dawadi/latex/control.json')+'">Project configuration in Git →</a></li><li><a href="'+esc(REPO_URL+'/blob/main/researchers/safal-dawadi/latex/source-baseline.json')+'">Source conflict register →</a></li><li><a href="../../../controls/latex/index.html">Shared LaTeX control tower →</a></li><li><a href="'+esc(drive_url(baseline["first_drive_published"]["source_zip_id"]))+'">Drive v1.9 source ZIP →</a></li><li><a href="'+esc(drive_url(baseline["first_drive_published"]["pdf_id"]))+'">Drive v1.9 review PDF →</a></li></ul></section><section class="section"><h2>Exact next boundary</h2><p>User selected latest v1.9 Local seq15. Verify actual final same-ID Drive ZIP/PDF bytes and reported SHA-256, import faithful admitted LaTeX into R&D Git, compile with the shared template, run full-page QA, and preserve Main cursor5 until separately acknowledged.</p></section></main>'

    current_candidate=baseline["latest_manifest_designated_candidate"]
    research_body=research_body.replace("</main>",'<section class="section"><h2>Current manifest-designated Midterm preview</h2><p>October 2026 v1.2 Midterm; 28 pages, non-production Tinos fallback. No new empirical evidence or university font certification. <a href="'+esc(drive_url(current_candidate["source_zip_id"]))+'">Source ZIP →</a> · <a href="'+esc(drive_url(current_candidate["pdf_id"]))+'">Preview PDF →</a></p><h3>Parallel v1.9 QA review</h3><p>42-page Local seq15 latest review explicitly selected (Q1 B); same-ID Drive source/PDF mirror and SHA readback still required before Git admission. Main ACK for seq15 not independently verified. Main registry last recorded Safal row remains seq2.</p></section></main>')
    write(out,"researchers/safal-dawadi/latex/index.html",shell("Safal LaTeX Governance",research_body,3))

    how=f'''<main class="wrap hero"><div class="eyebrow">ChatGPT operating path</div><h1>How to use this repository</h1><section class="section"><div class="flow"><div class="node">Choose researcher</div><div class="arrow">→</div><div class="node">Choose lane</div><div class="arrow">→</div><div class="node">Read shared control</div><div class="arrow">→</div><div class="node">Work in branch</div></div></section><section class="section"><h2>External output flow</h2><p class="lead">Build/render → upload output to Google Drive → read back the Drive ID/link → update the lane pointer JSON → commit. Git commit history replaces routine duplicate PRE/POST archive copies.</p></section><section class="section"><h2>Presentation recommendation</h2><p>Default to <strong>TypeScript + PptxGenJS + YAML/JSON</strong> for editable presentations. HTML/CSS/SVG may be used for PDF-first rendering. Generated PPTX/PDF files belong in Drive, not Git.</p></section></main>'''
    write(out,"how-to/index.html",shell("How to",how,1))
    data_dir=out/"data"; data_dir.mkdir()
    for src,name in [(ROOT/"registry/researchers.json","researchers.json"),(ROOT/"registry/branch-registry.json","branch-registry.json"),(ROOT/"registry/websites.json","websites.json"),(ROOT/"registry/debts.json","debts.json"),(ROOT/"controls/repository.control.json","repository-policy.json")]:
        shutil.copy2(src,data_dir/name)
    shutil.copy2(ROOT/"registry/researcher-folder-roles.json",data_dir/"researcher-folder-roles.json")
    shutil.copy2(ROOT/"registry/latex-build-profiles.json",data_dir/"latex-build-profiles.json")
    print(f"built {out} researchers={len(researchers)}")

if __name__=="__main__": main()
