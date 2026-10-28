"""A9 document-engineering static pages; data-only, no private document ingestion."""
from pathlib import Path
from site_core import REPO_URL, esc, load, shell, write

def build_document_pages(out):
    c=load(Path("registry/enterprise-document-catalog.json"))
    current=load(Path("registry/enterprise-document-types.json"))
    cards="".join('<article class="card"><h3>'+esc(x["title"])+'</h3><p class="muted">Approved template layout · actual documents require review</p><p><a href="'+esc(REPO_URL+"/blob/main/"+x["path"])+'">View LaTeX →</a></p></article>' for x in current["templates"])
    categories="".join('<li>'+esc(a)+': '+str(b)+'</li>' for a,b in c["categories"])
    enterprise=('<main class="wrap hero"><div class="eyebrow">A9 · Document Engineering</div><h1>Enterprise Documents</h1>'
      '<p class="lead">Contracts, experience letters, salary agreements, quotations, purchase orders, vouchers, estimates and proposals. '
      'One reusable code library for Fishtail, Rohini, Paila Pilates and other organizations; restricted source records remain in Drive.</p>'
      '<section class="section"><h2>Reusable source templates</h2><div class="grid">'+cards+'</div></section>'
      '<section class="section"><h2>Version 3: Enterprise control tower</h2>'
      '<p>14 uniquely routed and layout-approved templates, one shared LaTeX style, eight release gates, source-first provenance. Private document issuance still requires independent review.</p>'
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
    enterprise=enterprise.replace('</main>',
      '<section class="section"><h2>Template normalization QA</h2>'
      '<p>Fourteen v3 template layouts are approved; five older/variant sources remain preserved as historical references. '
      'No files have been removed.</p>'
      '<p><a href="template-audit/index.html">Review template collisions and variants →</a></p></section></main>')
    enterprise=enterprise.replace('</main>',
      '<section class="section"><h2>Structural Analysis and Design Report — new draft candidate</h2>'
      '<p>Public-safe LaTeX report layout and deterministic draft renderer. Numerical methods, solver runs, NBC checks, '
      'member design and validation are owned by the separate JP Structural Analysis engine; private precedents stay in Drive.</p>'
      '<p><strong>State:</strong> New candidate, not one of the fourteen approved V3 template routes; no completed engineer-approved SAR.</p>'
      '<p><a href="https://github.com/FabinGurung/JP_Research-and-Development/blob/main/templates/enterprise/structural-analysis-report/v0.1/README.md">Read the template and usage →</a> · '
      '<a href="https://github.com/FabinGurung/JP_Research-and-Development/blob/main/templates/enterprise/structural-analysis-report/v0.1/main.tex">LaTeX source →</a> · '
      '<a href="https://github.com/FabinGurung/JP_Structural_Analysis/">Analysis engine →</a></p>'
      '</section></main>')
    enterprise=enterprise.replace('</main>',
      '<section class="section"><h2>Contracts with traceable source appendices</h2>'
      '<p>A construction agreement should normally be delivered separately from original drawing PDFs and the materials/workmanship schedule. '
      'Agreement A references source drawings B by sheet/page and the separately approved materials C; drawn scope is not automatically included. '
      'Only restricted Drive holds real client files; public Pages contains reusable method and code only.</p>'
      '<p><a href="source-backed-contracts/">View source-to-scope documentation and checks →</a> · '
      '<a href="'+esc(REPO_URL+'/blob/main/docs/document-engineering/CONSTRUCTION_AGREEMENT_THREE_DOCUMENT_STANDARD.md')+'">Three-file A/B/C material standard →</a></p></section></main>')
    write(out,"enterprise-documents/index.html",shell("Enterprise Documents",enterprise,1))
    source_body=(
      '<main class="wrap hero"><div class="eyebrow">A9 · Enterprise Document Engineering</div>'
      '<h1>Source-backed construction agreements</h1>'
      '<p>Document A: agreement. Document B: architectural/structural source drawings with exact sheet citations. Document C: materials and workmanship schedule with brands and approved equivalents. None is silently merged with another.</p>'
      '<p class="lead">Original drawings stay in their authoritative storage. Client agreements can link and cite exact source sheets, while keeping actual approved commercial scope explicit.</p>'
      '<p><a href="'+esc(REPO_URL+'/blob/main/docs/document-engineering/CONSTRUCTION_AGREEMENT_THREE_DOCUMENT_STANDARD.md')+'">Read reusable three-document creation rules and materials specification fields →</a></p>'
      '<section class="section"><h2>Source-to-scope chain</h2><div class="flow">'
      '<div class="node">Original private drawings</div><div class="arrow">→</div>'
      '<div class="node">Sheet-level citations</div><div class="arrow">→</div>'
      '<div class="node">Contract scope and VOs</div><div class="arrow">→</div>'
      '<div class="node">Three separate A / B / C files</div></div></section>'
      '<section class="section"><h2>Review boundaries</h2><p>A source drawing being available does not mean it is signed or issue-for-construction. '
      'Plumbing, electrical, compound and railing work may require mutually agreed details. Variations have no invented prices. '
      'Milestone amounts must reconcile to the base total even where printed percentages are rounded.</p></section>'
      '<section class="section"><h2>Versioning and client copies</h2><p>Public Git owns reusable LaTeX layouts, schema, generator, validation tests and deployment code. '
      'Private Drive owns per-client editable TeX, compiled PDF, signed copies, the source drawing binary and internal review notes. '
      'Client copies use ordinary agreement names; internal QA and lifecycle status are retained separately, and execution requires real signatures.</p></section>'
      '<section class="section"><h2>Inspect the reusable controls</h2><p>'
      '<a href="'+esc(REPO_URL+'/blob/main/schemas/enterprise/client-contract-instance.schema.json')+'">Semantic source-citation schema →</a> · '
      '<a href="'+esc(REPO_URL+'/blob/main/controls/document-engineering/client-contract-reusable-clauses.policy.v1.json')+'">Reusable agreement clauses →</a> · '
      '<a href="'+esc(REPO_URL+'/actions/workflows/enterprise-contract-source-evidence.yml')+'">Synthetic source-evidence QA workflow →</a></p>'
      '<p>No private project PDF or private construction facts are embedded here.</p></section></main>'
    )
    write(out,"enterprise-documents/source-backed-contracts/index.html",shell("Source-backed Construction Agreements",source_body,2))



    tower=load(Path("controls/document-engineering/tower.json"))
    typed=load(Path("registry/enterprise-document-types.json"))["templates"]
    cards2="".join('<article class="card"><h3>'+esc(m["title"])+'</h3>'
      '<p class="muted">Template layout approved · project issuance requires review</p>'
      '<p><a href="'+esc(REPO_URL+"/blob/main/controls/document-engineering/types/"+m["id"]+".json")+'">Semantic fields and gates →</a> '
      '· <a href="'+esc(REPO_URL+"/blob/main/"+m["path"])+'">LaTeX source →</a></p></article>'
      for m in typed)
    gates=tower["release_gates"]
    gatecards="".join('<article class="card"><h3>'+esc(g)+'</h3>'
       '<p>Blocked until verified by the correct technical/human authority.</p></article>' for g in gates)
    body=('<main class="wrap hero"><div class="eyebrow">A9 · Enterprise Document Engineering v3</div>'
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
      '<a href="'+esc(REPO_URL+'/blob/main/scripts/document_engineering/engine_v3.py')+'">Draft renderer →</a> · '
      '<a href="'+esc(REPO_URL+'/actions/workflows/enterprise-document-v2.yml')+'">Source QA workflow →</a></p>'
      '<p><strong>Not certified:</strong> complete legal/technical parity, actual company documents, human signatures and every-page visual QA.</p>'
      '</section></main>')
    write(out,"enterprise-documents/control-tower/index.html",shell("Enterprise Document Control Tower",body,2))


    audit=load(Path("registry/enterprise-template-normalization-audit.v0.1.json"))
    rows="".join(
        '<tr><td>'+str(t["position"])+'</td><td>'+esc(t["title"])+'</td>'
        '<td><code>'+esc(t["type_id"])+'</code></td>'
        '<td><a href="'+esc(REPO_URL+'/blob/main/'+t["path"])+'">Source</a></td>'
        '<td>'+esc(t["decision"])+'</td></tr>' for t in audit["canonical"])
    extras="".join(
        '<tr><td>'+esc(x["id"])+'</td><td>'+esc(x["family"])+'</td>'
        '<td><a href="'+esc(REPO_URL+'/blob/'+x.get("branch","main")+'/'+x["path"])+'">Inspect</a></td>'
        '<td>'+esc(x["classification"])+'</td><td>'+esc(x["decision"])+'</td></tr>'
        for x in audit["overlaps"])
    audit_body=(
        '<main class="wrap hero"><div class="eyebrow">Enterprise Documents · Human QA</div>'
        '<h1>Template normalization inventory</h1>'
        '<p class="lead">Fourteen callable document types, three legacy prototypes and two client-contract variants.'
        ' Related filenames are not evidence of identical source. Nothing has been deleted or merged.</p>'
        '<section class="section"><h2>Canonical draft types (14)</h2>'
        '<div class="table-scroll"><table><thead><tr><th>No.</th><th>Type</th><th>ID</th><th>Source</th><th>Review state</th></tr></thead>'
        '<tbody>'+rows+'</tbody></table></div></section>'
        '<section class="section"><h2>Overlaps and variants to QA (5)</h2>'
        '<div class="table-scroll"><table><thead><tr><th>Candidate</th><th>Family</th><th>Source</th><th>Classification</th><th>Review state</th></tr></thead>'
        '<tbody>'+extras+'</tbody></table></div></section>'
        '<section class="section"><h2>Before any cleanup</h2>'
        '<p>Compare semantics, required fields, rendering, data security and legal approvals. Retain historical Git SHAs, '
        'original Overleaf sources and private project revisions. Approve canonical IDs and variant names individually.</p>'
        '<p><a href="'+esc(REPO_URL+'/blob/main/registry/enterprise-template-normalization-audit.v0.1.json')+
        '">Open machine-readable audit →</a></p></section></main>')
    write(out,"enterprise-documents/template-audit/index.html",shell("Enterprise Template QA",audit_body,2))
