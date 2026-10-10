# A9 Document Engineering

## Current live position
Enterprise Documents and Academic Writing are separate public-safe R&D website pages.
The original Overleaf archive has 102 items (73 .tex, 24 images, 4 PDF, one extensionless file).
SHA-256: a0986692274647b68b3c839c4be0d827e55345f5502c6e67bab4c4dd61efc924.
Private Drive original ID: 1wW-_B6bvETGFN_L7XMWcBZlUYBMTqzFP.
A9 shared Document Engineering folder ID: 1QEP_J-qvUIRX2rKzlJscJRXnTOuxjcRr.

## Public vs private
- Git: executable generic LaTeX templates, safe fake data, static pages, controls and rollback history.
- Drive: source ZIP, private contract precedents, payroll details, original images/PAN/licenses, private per-company inputs and signed outputs.
- Never commit a real contract or confidential PDF, a personal JSON file or signature asset to public Git or Actions.
- The extracted private source is SHA-256 classified locally; file-level Drive ingestion/readback is pending, and no PDF is certified by this release.

## Source build
1. Choose a template_id: works-contract, experience-letter or salary-contract.
2. Fill all fields defined in scripts/document_engineering/build.py in a private JSON document.
3. Generate TeX with the command below. The sample is fictional.
4. For local PDF compilation only, add --compile and install latexmk/TeX Live.
5. Verify company, project, personnel authority and all agreement terms, then use human approval/signing.
6. Save accepted output in the company's/project's live Drive and register the returned ID.

    python3 scripts/document_engineering/build.py --data examples/document-engineering/sample_works_contract.json --out /tmp/a9-doc-test

Templates are DRAFTS requiring legal, labour, tax and engineering review. Do not assume historical Overleaf projects compile cleanly without graphics/fonts or license checks.

## Academic writing
The academic tower remains controls/latex/tower.json and controls/latex/template/pumlsc-shared.sty. Enterprise document source is never another academic thesis control tower.

## Existing ZIP categories
The public machine-readable family summary is in registry/enterprise-document-catalog.json. Actual client-specific filenames and per-item hashes belong in the private Drive audit manifest, not the public repository.
