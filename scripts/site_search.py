#!/usr/bin/env python3
"""Build searchable PUBLIC portal metadata. No Drive reads; no scientific inference."""
from __future__ import annotations
import json
from site_core import REPO_URL,esc,write,shell,branch_url

def build_index(researchers, branches, websites):
    entries=[]
    def add(kind,title,description,url,keywords="",status="REFERENCE"):
        entries.append({
            "category":kind,"title":title,"description":description,"url":url,
            "keywords":keywords,"status":status
        })
    add("Documentation","Start here: read, verify, build",
        "Operating guide: Git source, Drive boundaries, A9 procedures and researcher scope.",
        "../start-here/index.html","onboarding guide roadmap workflow")
    add("Documentation","Thesis infrastructure and folder roles",
        "Point-in-time verified folder roles, reusable project controls and scientific boundaries.",
        "../thesis-infrastructure/index.html","drive folders governance thesis controls")
    add("Documentation","R&D roadmap and holds",
        "Developed components, next engineering tasks and intentionally held work.",
        "../roadmap/index.html","roadmap next debt status")
    add("Documentation","Open research debts",
        "Known open and held research questions; does not authorize resuming any HOLD.",
        "../debts/index.html","hold risk scientific audit")
    add("Documentation","Git branch history explorer",
        "Historical branch inventory; observations are not real-time git ref verification.",
        "../branches/index.html","git version snapshots archives rollback")
    for x in researchers:
        rid=x["researcher_id"]
        slug=x["slug"]
        name=x["display_name"]
        topic=x.get("topic_title") or "Thesis topic: human QA required"
        add("Researchers",name,topic,"../researchers/"+slug+"/index.html",
            rid+" "+slug+" thesis academic",x.get("qa_status","HOLD"))
        add("Handovers",name+" — researcher chat handover",
            "Copy-only manual prompt. Pasting it into the owner chat is required for any execution.",
            "../owner-prompts/"+slug+"/index.html",rid+" "+name+" researcher Drive governance owner normalization opt in","NOT_TRIGGERED")
    for key,label,descr in [
        ("latex","LaTeX and Pokhara University formatting","Canonical shared template, university source-rule parity and separate document approvals."),
        ("discussion","Research discussion control","Document pointers, governing discussion roles and review workflows."),
        ("presentation","Presentation production control","Reusable slide authoring policy and editable source."),
        ("website","Website control and publication","Static publication policy and verified optional researcher websites."),
    ]:
        add("Controls",label,descr,"../controls/"+key+"/index.html",key+" shared source governance template")
    for b in branches["branches"]:
        add("Git branches",b["name"],b.get("purpose") or "Observed repository branch",
            branch_url(b["name"]), (b.get("primary_source_path") or "")+" "+b["category"]+" "+b.get("source_status",""),
            "OBSERVED_"+branches["observed_date"])
    for web in websites:
        url=web.get("public_site_path")
        if url and url.startswith("/"):
            add("Research websites",web["label"]+" research module",
                "Registered research website module; inspect upstream for scientific claim status.",
                ".."+url+"index.html",web.get("researcher_slug","")+" "+web.get("module_slug","")+" "+web.get("state",""),
                web.get("state","HOLD"))
    for sub,title in [
        ("methodology-demo","AEC methodology interactive demo"),
        ("hydropower-data-model","Hydropower data model"),
        ("hydropower-data-schema","Hydropower data schema"),
        ("hydropower-data-tables","Hydropower data tables"),
        ("hydropower-data-graph","Hydropower data graph"),
        ("hydropower-nepal-map","Hydropower Nepal geography map")
    ]:
        add("Research demos",title,"Preserved historical public-safe standalone module.",
            "../"+sub+"/","hydropower aec research history legacy","HISTORICAL")
    for p,title,words in [
        ("docs/REPO_ONLY_NEXT_STEPS_20261009.md","Repository-only maintenance roadmap","code architecture QA browser"),
        ("docs/OWNER_HANDOVERS_AND_LIBRARY_THEME_V2_20261009.md","Owner handovers and visual theme release","visual winged book safe"),
        ("docs/UNIVERSAL_THESIS_BUILD_READ_FIRST_20261009.md","Authorized universal thesis build runbook","xelatex biber source QA"),
        ("docs/THESIS_FOLDER_NORMALIZATION_GAP_MATRIX_20261009.md","Thesis folder normalization gap matrix","researcher folder gap"),
        ("docs/THESIS_INFRASTRUCTURE_RELEASE_20261009.md","Thesis infrastructure checkpoint","latex source registry")
    ]:
        add("Documentation",title,"Version-controlled central repository guide.",
            REPO_URL+"/blob/main/"+p,words,"GIT_DOCUMENT")
    return {
      "schema_version":"1.0.0",
      "description":"Public-safe metadata index; never contains private thesis text or live provider guarantees.",
      "git_branch_observation_date":branches["observed_date"],
      "entries":entries,
    }

def render_search(out,researchers,branches,websites):
    index=build_index(researchers,branches,websites)
    write(out,"data/research-index.json",json.dumps(index,ensure_ascii=False,indent=2)+"\n")
    body='<main class="wrap hero"><div class="eyebrow">Reading-room catalogue</div><h1>Find a researcher, source or control.</h1>'
    body+='<p class="lead">Search the published R&D catalogue: researchers, owning chat handovers, the single shared control tower, observed Git branches, research websites and durable runbooks. Links are snapshots; recheck live Git and Drive before edits.</p>'
    body+='<section class="section"><div class="search-box"><label for="research-search">Search library</label>'
    body+='<input type="search" id="research-search" placeholder="Try Safal, seismic, LaTeX, Git history…" autocomplete="off" aria-describedby="search-help">'
    body+='<p id="search-help" class="muted">Press / to search and Escape to clear. Search is local to the website; your query is not transmitted to a server.</p>'
    body+='<label for="research-category">Filter by collection</label><select id="research-category"><option value="">All collections</option></select>'
    body+='<div class="search-summary" id="search-summary" role="status" aria-live="polite">Loading catalogue…</div></div>'
    body+='<div id="research-results" class="search-results" aria-label="Search results"></div>'
    body+='<button id="research-more" class="motion-toggle" type="button" hidden>Show more results</button>'
    body+='<noscript><p>The search interface requires JavaScript. <a href="../researchers/index.html">Browse researchers</a> or <a href="../branches/index.html">browse Git branches</a>.</p></noscript>'
    body+='</section><section class="section"><div class="notice">A matching record is a discovery link, not scientific approval. Researcher migration prompts remain inert until pasted by the user in their owning chat.</div></section></main>'
    write(out,"search/index.html",shell("Search Research",body,1))
    return index
