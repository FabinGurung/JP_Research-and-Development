# Historical v1 prototype — Superseded by v2

This document describes the initial three-template prototype and is retained for reproducibility. Use [Enterprise Document Engineering v2](DOCUMENT_ENGINEERING_V2_READ_FIRST.md) for the current fourteen-type draft engine. No old client contract is production certified.

---

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
- The extracted private source is SHA-256 classified locally; 102 of 102 original source entries were uploaded as separate Google Drive files with provider file ID, path/name and byte-size readback. Remote byte-level SHA-256 comparison has not been run for all items, and no contract is legally certified by this release.

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

## Governed private source ingestion
File-level ingestion **completed** through an authenticated connected Google Drive library operation. The idempotent Colab/local runner remains available for independent deep MD5 readback and future imports, but **DO NOT execute it just to re-upload the same archive**:

    python3 scripts/document_engineering/ingest_zip_drive.py --config examples/document-engineering/private_ingest_routes.json --report /private/plan.json
    python3 scripts/document_engineering/ingest_zip_drive.py --config examples/document-engineering/private_ingest_routes.json --execute --report /private/readback.json

Default is dry run. --execute uploads only missing entries, checks SHA-256 of the original ZIP, compares pre-existing MD5 checksums and readbacks uploaded IDs/parents/checksums. Private report must not be committed to Git. This is a reference procedure for subsequent or MD5-hardening runs; current provider file-count, filenames, and byte sizes were checked in A9 Drive. Provider raw-byte per-file hashes are an optional deeper audit, not already completed.

## Completed archive readback and contract reference (2026-10-10)
- 102/102 raw files in the A9 private `02_EXTRACTED_PRIVATE_SOURCE` tree; all 16 leaf-directory listings checked with individual filenames and byte sizes.
- Original SHA-256 confirmed against the unchanged Overleaf ZIP, and local extracted per-file SHA-256s computed.
- Private full tree and QA notes: Drive file `1cTkhtadrjK6dFNwbiTFsNDn7kCcRRZ4Z`; private manifest: `1mBRpSFVSUdPZLHD-6asZ3vaNZsDc7SQe`.
- The two distinct `Pradip adhikari.tex` sources are preserved in separated subfolders, not overwritten.
- Bishal visual precedent: private `client_contracts/14client_BishalPaija.tex` MAIN agreement only. Its named parties/finances are never copied into public templates.
- Rohini–Radha Roka project has a separate 5-page DRAFT / NOT FOR SIGNATURE agreement in its own Rohini project Drive tree; it is not a public Git source, signed record, or approved legal contract.
