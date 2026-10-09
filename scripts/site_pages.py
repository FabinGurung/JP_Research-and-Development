#!/usr/bin/env python3
"""Reusable editorial pages for R&D; source authority and URLs unchanged."""
from __future__ import annotations
from site_core import ROOT,REPO_URL,esc,write,shell

def build_home(researchers,folder_roles):
    home_cards="".join(f'<article class="card"><span class="badge">{esc("TITLE VERIFIED · OTHER POINTERS HOLD" if r["qa_status"]=="TITLE_VERIFIED_OTHER_POINTERS_HOLD" else "ON HOLD · HUMAN QA")}</span><h3>{esc(r["display_name"])}</h3><p>{esc(r.get("topic_title") or "Topic/title and Drive pointers are intentionally unset.")}</p><a href="researchers/{esc(r["slug"])}/index.html">Open researcher workspace →</a></article>' for r in researchers)
    home=f'''<main><section class="wrap hero"><div class="eyebrow">Research control portal</div><h1>JP Research & Development</h1><p class="lead">One thin main branch for shared controls, researcher routing and verified Drive links. Research documents and generated outputs stay in Google Drive; code changes are tracked on full-repository Git branches; researcher paths are logical work areas.</p><p><span class="badge">{len(researchers)} researcher workspaces · selective human QA</span></p></section><section class="wrap section"><h2>Operating architecture</h2><div class="flow"><div class="node">Shared controls</div><div class="arrow">→</div><div class="node">Researcher index</div><div class="arrow">→</div><div class="node">Discussion / LaTeX / Presentation lanes</div><div class="arrow">→</div><div class="node">Google Drive outputs</div></div></section><section class="wrap section"><h2>Researchers</h2><div class="grid">{home_cards}</div></section><section class="wrap section"><h2>Boundaries</h2><div class="controls"><article class="card"><h3>GitHub main</h3><p>Portal code, controls, schemas, registries and links only.</p></article><article class="card"><h3>Researcher branches</h3><p>Discussion pointers, LaTeX source, presentation source/config.</p></article><article class="card"><h3>Google Drive</h3><p>Working Docs, compiled PDFs, generated PPTX/PDF and evidence.</p></article></div></section></main>'''
    old_intro_start=home.index('<section class="wrap hero">')
    old_intro_end=home.index("</section>",old_intro_start)+len("</section>")
    new_intro=(ROOT/"web/living-hero.html").read_text(encoding="utf-8")
    new_intro=new_intro.replace("@@RESEARCHERS@@",str(len(researchers))).replace("@@ROOTS@@",str(folder_roles["verified_root_count"]))
    home=home[:old_intro_start]+new_intro+home[old_intro_end:]
    home=home.replace("</main>",'<section class="wrap section"><h2>Search the R&D catalogue</h2><p>Find researchers, source policies, documents and observed Git branches in one public-safe reading-room index.</p><p><a href="search/index.html">Search research library →</a></p></section></main>')
    home=home.replace("</main>",'<section class="wrap section"><h2>New here? A guided entry point</h2><p>Learn which source controls each task, which checks are truly automated, and what is deliberately waiting for research/project approval.</p><p><a href="start-here/index.html">Open the six-step repository guide →</a></p></section></main>')
    home=home.replace("</main>",'<section class="wrap section"><h2>Paste-ready researcher handovers</h2><p>One opt-in prompt for each researcher — no migration begins until you paste it into that researcher’s own chat.</p><p><a href="owner-prompts/index.html">Choose and copy a handover →</a></p></section></main>')
    home=home.replace("</main>",'<section class="wrap section"><h2>Unified thesis infrastructure</h2><p>Browse verified project folder roles, source-control policy, university formatting engine and individual researcher handovers. No Drive folders were renamed or moved.</p><p><a href="thesis-infrastructure/index.html">Open thesis folder and automation map →</a></p></section></main>')
    return home

def render_start_here(out):
    # Reader-friendly repo-only operating guide: no scientific or A9 claims.
    start_cards=[
       ("0. Search the research library","Find researchers, shared controls, public documentation and Git history.","../search/index.html"),
       ("1. Explore the library","Browse eleven researcher identities, their public-safe source pointers and verified folders.","../researchers/index.html"),
       ("2. Read the shared control towers","Review thesis-wide PU formatting, versioning, scientific boundaries and repeatability requirements.","../controls/latex/index.html"),
       ("3. Copy an owner-specific handover","Pick a researcher prompt. Copying is inert; only pasting it into that owner's chat authorizes bounded work.","../owner-prompts/index.html"),
       ("4. Inspect the Git change history","Compare PRE and POST commits, known branch roles and archived ref identities.","../branches/index.html"),
       ("5. Check code validation and deployment","Open current GitHub Actions results; a green code gate never means a thesis PDF is scientifically approved.","https://github.com/FabinGurung/JP_Research-and-Development/actions"),
       ("6. Work on repo code, not Drive data","Improve UI, documentation, tests, generators and machine control without migrating databases or files.","https://github.com/FabinGurung/JP_Research-and-Development/blob/main/docs/REPO_ONLY_NEXT_STEPS_20261009.md"),
    ]
    start_items="".join(
       '<article class="card"><h3>'+esc(title)+'</h3><p>'+esc(detail)+'</p><a href="'+esc(link)+'">Open →</a></article>'
       for title,detail,link in start_cards
    )
    start_body='<main class="wrap hero"><div class="eyebrow">R&D · operating guide</div><h1>Start here: read, verify, build.</h1>'
    start_body+='<p class="lead">Use one source of truth for each concern: Git for authorized code and history; Drive for scientific evidence and documents; the owning researcher for project decisions; A9 for registrations and acknowledgments.</p>'
    start_body+='<div class="notice"><strong>Current scope:</strong> repository quality and website usability. <strong>Deferred:</strong> database and Drive migrations, research-source edits, project-local A9 synchronization, scientific review and production PDF certification.</div>'
    start_body+='<section class="section"><h2>Choose a workflow</h2><div class="grid">'+start_items+'</div></section>'
    start_body+='<section class="section"><h2>How to interpret a green build</h2><p>Repository validation checks source contracts, generated site links, owner handovers and reusable LaTeX source gates. A successful GitHub Pages deployment confirms publication of the static site, not a screenshot-level design review or scientific thesis approval.</p></section>'
    start_body+='<section class="section"><h2>Non-destructive operating rules</h2><p>Preserve all existing Git branches, archived artifacts, original Drive IDs and approved research versions. Never trigger researcher workspace migration merely because it is listed on this site.</p></section></main>'
    write(out,"start-here/index.html",shell("Start Here",start_body,1))

def render_owner_prompt(out,r,owner_by_id):
        source=ROOT/"prompts/researchers"/(r["researcher_id"]+"__"+r["slug"]+".md")
        prompt=source.read_text(encoding="utf-8")
        status=owner_by_id[r["researcher_id"]]["state"]
        prompt_body='<main class="wrap hero"><div class="eyebrow">Researcher chat execution · deliberate opt-in</div><h1>'+esc(r["display_name"])+'</h1>'
        prompt_body+='<p class="lead">Copy this complete, researcher-specific handover and paste it only in the researcher’s original chat. This website does not execute migrations or make Drive changes.</p>'
        prompt_body+='<div class="notice"><strong>'+esc(r["researcher_id"])+'</strong> · '+esc(status)+' · NO DELETE · NO MAIN ACK</div>'
        prompt_body+='<section class="section owner-prompt-desk"><div class="owner-prompt-top"><h2>Full owner-chat handover</h2><p><a href="'+esc(REPO_URL+"/blob/main/prompts/researchers/"+r["researcher_id"]+"__"+r["slug"]+".md")+'">Verify Git source →</a></p></div>'
        prompt_body+='<textarea id="owner-prompt-text" readonly aria-label="Researcher-specific migration prompt" spellcheck="false">'+esc(prompt)+'</textarea>'
        prompt_body+='<div class="copy-owner-row"><button class="owner-copy-button" type="button" data-copy-owner-prompt="owner-prompt-text">Copy entire prompt</button><span class="owner-copy-status" data-copy-status aria-live="polite">Paste in this researcher’s chat only.</span></div></section>'
        prompt_body+='<p><a href="../../owner-prompts/index.html">← All owner handovers</a></p></main>'
        write(out,f'owner-prompts/{r["slug"]}/index.html',shell(r["display_name"]+" — Owner handover",prompt_body,2))

def render_owner_directory(out,researchers,owner_by_id):
    owner_cards="".join('<article class="card"><h3>'+esc(x["researcher_id"]+" · "+x["display_name"])+'</h3><p>'+esc(owner_by_id[x["researcher_id"]]["state"])+'</p><a href="'+esc(x["slug"]+"/index.html")+'">Read and copy full prompt →</a></article>' for x in researchers)
    owner_body='<main class="wrap hero"><div class="eyebrow">11 individual researcher handovers</div><h1>A handover reading desk</h1><p class="lead">Each owner-only prompt is inactive until you copy and paste it in that researcher’s chat. No deletion, no mass Drive migration, no scientific edits.</p>'
    owner_body+='<div class="notice">RSH-004 remains a read-only HOLD until its project root is verified. All others require fresh Drive readback, PRE/POST and owner-specific authority.</div>'
    owner_body+='<section class="section"><div class="grid">'+owner_cards+'</div></section></main>'
    write(out,"owner-prompts/index.html",shell("Owner Chat Handovers",owner_body,1))
