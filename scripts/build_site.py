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
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · JP R&D</title><link rel="stylesheet" href="{prefix}assets/styles.css"></head><body><header class="topbar"><div class="wrap nav"><strong>JP R&D</strong><nav class="navlinks"><a href="{prefix}index.html">Home</a><a href="{prefix}researchers/index.html">Researchers</a><a href="{prefix}workspace/index.html">Workspace</a><a href="{prefix}controls/index.html">Controls</a><a href="{prefix}debts/index.html">Debts</a><a href="{prefix}how-to/index.html">How to</a></nav></div></header>{body}<footer class="wrap footer">JP Research & Development · code + controls + pointers · working artifacts remain in Google Drive.</footer></body></html>"""

def write(out, rel, content):
    p=out/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content,encoding="utf-8")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",default="dist"); args=ap.parse_args()
    out=ROOT/args.out
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    researchers=load(Path("registry/researchers.json"))["researchers"]
    websites=load(Path("registry/websites.json"))["websites"]
    branches=load(Path("registry/branch-registry.json"))
    policy=load(Path("controls/repository.control.json"))
    controls={
      "Discussion":load(Path("controls/discussion.control.json")),
      "LaTeX":load(Path("controls/latex.control.json")),
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
    (out/"assets").mkdir(); shutil.copy2(ROOT/"web/styles.css",out/"assets/styles.css")
    (out/".nojekyll").write_text("",encoding="utf-8")
    # Restore the original public-safe standalone demos into the ONE main Pages deployment.
    # Source blobs retain the archived Git IDs and are immutable until separately revised.
    legacy=ROOT/"web/legacy-site"
    for site_name in ("methodology-demo","hydropower-data-model","hydropower-data-schema","hydropower-data-tables","hydropower-data-graph","hydropower-nepal-map"):
        src=legacy/site_name
        if src.is_dir(): shutil.copytree(src,out/site_name,dirs_exist_ok=True)
    home_cards="".join(f'<article class="card"><span class="badge">{esc("TITLE VERIFIED · OTHER POINTERS HOLD" if r["qa_status"]=="TITLE_VERIFIED_OTHER_POINTERS_HOLD" else "ON HOLD · HUMAN QA")}</span><h3>{esc(r["display_name"])}</h3><p>{esc(r.get("topic_title") or "Topic/title and Drive pointers are intentionally unset.")}</p><a href="researchers/{esc(r["slug"])}/index.html">Open researcher workspace →</a></article>' for r in researchers)
    home=f'''<main><section class="wrap hero"><div class="eyebrow">Research control portal</div><h1>JP Research & Development</h1><p class="lead">One thin main branch for shared controls, researcher routing and verified Drive links. Research documents and generated outputs stay in Google Drive; source code lives in governed researcher lanes.</p><p><span class="badge">{len(researchers)} researcher workspaces · selective human QA</span></p></section><section class="wrap section"><h2>Operating architecture</h2><div class="flow"><div class="node">Shared controls</div><div class="arrow">→</div><div class="node">Researcher index</div><div class="arrow">→</div><div class="node">Discussion / LaTeX / Presentation lanes</div><div class="arrow">→</div><div class="node">Google Drive outputs</div></div></section><section class="wrap section"><h2>Researchers</h2><div class="grid">{home_cards}</div></section><section class="wrap section"><h2>Boundaries</h2><div class="controls"><article class="card"><h3>GitHub main</h3><p>Portal code, controls, schemas, registries and links only.</p></article><article class="card"><h3>Researcher branches</h3><p>Discussion pointers, LaTeX source, presentation source/config.</p></article><article class="card"><h3>Google Drive</h3><p>Working Docs, compiled PDFs, generated PPTX/PDF and evidence.</p></article></div></section></main>'''
    write(out,"index.html",shell("Home",home,0))
    directory="".join(f'<article class="card"><h3>{esc(r["display_name"])}</h3><p><span class="badge">{esc(r["qa_status"])}</span></p><p>{esc(r.get("topic_title") or "Topic title: ON HOLD")}</p><a href="{esc(r["slug"])}/index.html">Open →</a></article>' for r in researchers)
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
        write(out,f'researchers/{r["slug"]}/index.html',shell(r["display_name"],body,2))
        if researcher_debts:
            debt_cards=""
            for d in researcher_debts:
                evidence=evidence_html(d)
                debt_cards+=f'<article class="card"><span class="badge">{esc(d["status"])}</span><h3>{esc(d["title"])}</h3><p>{esc(d["description"])}</p><p><strong>Category:</strong> {esc(d["category"])} · <strong>Severity:</strong> {esc(d["severity"])}</p><ul>{evidence}</ul><p><strong>Close when:</strong> {esc(d["close_when"])}</p></article>'
            debt_body=f'<main class="wrap hero"><div class="eyebrow">{esc(r["researcher_id"])} · governed debt</div><h1>{esc(r["display_name"])} — Research Debts</h1><p class="lead">Only verified open/held debt is listed here. Closing an item requires provider-read evidence and an updated registry state.</p><div class="grid">{debt_cards}</div><p><a href="../index.html">← Back to researcher workspace</a></p></main>'
            write(out,f'researchers/{r["slug"]}/debts/index.html',shell(f'{r["display_name"]} Debts',debt_body,3))
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
        body=f'<main class="wrap hero"><div class="eyebrow">Shared control</div><h1>{name}</h1><div class="kvs"><div>Control ID</div><div class="code">{esc(c["control_id"])}</div><div>Status</div><div>{esc(c["status"])}</div><div>Branch pattern</div><div class="code">{esc(c["branch_pattern"])}</div><div>Authority</div><div>{esc(c["authority"])}</div></div><section class="section"><h2>Workflow</h2><ol>'+''.join(f'<li>{esc(x)}</li>' for x in c["workflow"])+'</ol></section></main>'
        write(out,f"controls/{slug}/index.html",shell(name,body,2))
    how=f'''<main class="wrap hero"><div class="eyebrow">ChatGPT operating path</div><h1>How to use this repository</h1><section class="section"><div class="flow"><div class="node">Choose researcher</div><div class="arrow">→</div><div class="node">Choose lane</div><div class="arrow">→</div><div class="node">Read shared control</div><div class="arrow">→</div><div class="node">Work in branch</div></div></section><section class="section"><h2>External output flow</h2><p class="lead">Build/render → upload output to Google Drive → read back the Drive ID/link → update the lane pointer JSON → commit. Git commit history replaces routine duplicate PRE/POST archive copies.</p></section><section class="section"><h2>Presentation recommendation</h2><p>Default to <strong>TypeScript + PptxGenJS + YAML/JSON</strong> for editable presentations. HTML/CSS/SVG may be used for PDF-first rendering. Generated PPTX/PDF files belong in Drive, not Git.</p></section></main>'''
    write(out,"how-to/index.html",shell("How to",how,1))
    data_dir=out/"data"; data_dir.mkdir()
    for src,name in [(ROOT/"registry/researchers.json","researchers.json"),(ROOT/"registry/branch-registry.json","branch-registry.json"),(ROOT/"registry/websites.json","websites.json"),(ROOT/"registry/debts.json","debts.json"),(ROOT/"controls/repository.control.json","repository-policy.json")]:
        shutil.copy2(src,data_dir/name)
    print(f"built {out} researchers={len(researchers)}")

if __name__=="__main__": main()
