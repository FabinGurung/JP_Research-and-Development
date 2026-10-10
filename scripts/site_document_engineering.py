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
