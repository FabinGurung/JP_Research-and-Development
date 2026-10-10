"""A9 document-engineering static pages; data-only, no private document ingestion."""
from pathlib import Path
from site_core import REPO_URL, esc, load, shell, write

def build_document_pages(out):
    c=load(Path("registry/enterprise-document-catalog.json"))
    cards="".join('<article class="card"><h3>'+esc(x["name"])+'</h3><p class="muted">Draft source — approval required</p><p><a href="'+esc(REPO_URL+"/blob/main/"+x["path"])+'">View LaTeX →</a></p></article>' for x in c["templates"])
    categories="".join('<li>'+esc(a)+': '+str(b)+'</li>' for a,b in c["categories"])
    enterprise=('<main class="wrap hero"><div class="eyebrow">A9 · Document Engineering</div><h1>Enterprise Documents</h1>'
      '<p class="lead">Contracts, experience letters, salary agreements, quotations, purchase orders, vouchers, estimates and proposals. '
      'One reusable code library for Fishtail, Rohini, Paila Pilates and other organizations; restricted source records remain in Drive.</p>'
      '<section class="section"><h2>Reusable source templates</h2><div class="grid">'+cards+'</div></section>'
      '<section class="section"><h2>Version 2: Enterprise control tower</h2>'
      '<p>14 typed document modules, one shared LaTeX style, eight release gates, source-first provenance. All remain draft only, pending independent human approval.</p>'
      '<p><a href="control-tower/index.html">Explore the 14 document controls and validation gates →</a></p></section>'
      '<section class="section"><h2>Classified Overleaf archive: 102 source items</h2>'
      '<p><strong>Ingestion complete:</strong> 102/102 files verified by private Drive file paths, names and byte sizes. '
      'Original ZIP SHA-256 verified; remote hash comparison for each extracted file remains a deeper optional audit.</p>'
      '<p><a href="https://drive.google.com/file/d/1cTkhtadrjK6dFNwbiTFsNDn7kCcRRZ4Z/view">Open private interactive file tree / QA review (authorized Drive users only) →</a></p>'
      '<ul>'+categories+'</ul></section>'
      '<section class="section"><h2>Production lifecycle</h2><div class="flow"><div class="node">Select source</div><div class="arrow">→</div>'
      '<div class="node">Verify private facts</div><div class="arrow">→</div><div class="node">Generate TeX</div><div class="arrow">→</div>'
      '<div class="node">Compile & review</div><div class="arrow">→</div><div class="node">Approve & archive in Drive</div></div>'
      '<p><a href="'+esc(REPO_URL+'/blob/main/docs/DOCUMENT_ENGINEERING.md')+'">Operating instructions →</a></p></section></main>')
    write(out,"enterprise-documents/index.html",shell("Enterprise Documents",enterprise,1))
    academic=('<main class="wrap hero"><div class="eyebrow">A9 · Document Engineering</div><h1>Academic Writing</h1>'
      '<p class="lead">Thesis, manuscripts, journal papers, BibTeX, research reports and university publication standards.</p>'
      '<section class="section"><h2>Existing shared LaTeX authority</h2>'
      '<div class="grid"><article class="card"><h3>Format tower</h3><a href="'+esc(REPO_URL+'/blob/main/controls/latex/tower.json')+'">Shared LaTeX controls →</a></article>'
      '<article class="card"><h3>Research library</h3><a href="../researchers/index.html">Researcher workspaces →</a></article>'
      '<article class="card"><h3>Production build procedure</h3><a href="'+esc(REPO_URL+'/blob/main/docs/UNIVERSAL_THESIS_BUILD_READ_FIRST_20261009.md')+'">Compile guide →</a></article></div></section>'
      '<section class="section"><h2>Authority boundary</h2><p>University rules, supervisor approval, originals and generated PDFs are governed by the academic owner, not the enterprise contract templates.</p></section></main>')
    write(out,"academic-writing/index.html",shell("Academic Writing",academic,1))

    tower=load(Path("controls/document-engineering/tower.json"))
    typed=load(Path("registry/enterprise-document-types.v2.json"))["types"]
    cards2="".join('<article class="card"><h3>'+esc(m["title"])+'</h3>'
      '<p class="muted">Draft candidate · no human approval</p>'
      '<p><a href="'+esc(REPO_URL+"/blob/main/"+m["control"])+'">Semantic fields and gates →</a> '
      '· <a href="'+esc(REPO_URL+"/blob/main/"+m["template"])+'">LaTeX source →</a></p></article>'
      for m in typed)
    gates=tower["release_gates"]
    gatecards="".join('<article class="card"><h3>'+esc(g)+'</h3>'
       '<p>Blocked until verified by the correct technical/human authority.</p></article>' for g in gates)
    body=('<main class="wrap hero"><div class="eyebrow">A9 · Enterprise Document Engineering v2</div>'
      '<h1>Document Control Tower</h1>'
      '<p class="lead">One shared source engine, fourteen typed semantic branches, immutable source lineage, explicit HOLD gates and private Drive evidence.</p>'
      '<section class="section"><h2>Control route</h2>'
      '<div class="flow"><div class="node">Overleaf originals / Drive</div><div class="arrow">→</div>'
      '<div class="node">Typed semantic rules</div><div class="arrow">→</div>'
      '<div class="node">LaTeX draft renderer</div><div class="arrow">→</div>'
      '<div class="node">8 QA / approval gates</div><div class="arrow">→</div>'
      '<div class="node">Private approved output in Drive</div></div></section>'
      '<section class="section"><h2>Fourteen document modules</h2><div class="grid">'+cards2+'</div></section>'
      '<section class="section"><h2>Eight release gates</h2><div class="grid">'+gatecards+'</div></section>'
      '<section class="section"><h2>Semantic handrails and implementation</h2>'
      '<p><a href="'+esc(REPO_URL+'/blob/main/controls/document-engineering/semantic-handrails.v2.json')+'">Type-specific review and rejection rules →</a> · '
      '<a href="'+esc(REPO_URL+'/blob/main/scripts/document_engineering/engine_v2.py')+'">Draft renderer →</a> · '
      '<a href="'+esc(REPO_URL+'/actions/workflows/enterprise-document-v2.yml')+'">Source QA workflow →</a></p>'
      '<p><strong>Not certified:</strong> complete legal/technical parity, actual company documents, human signatures and every-page visual QA.</p>'
      '</section></main>')
    write(out,"enterprise-documents/control-tower/index.html",shell("Enterprise Document Control Tower",body,2))

