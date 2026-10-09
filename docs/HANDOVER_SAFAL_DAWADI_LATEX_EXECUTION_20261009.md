# Safal Dawadi — executable LaTeX chat handover (2026-10-09)

## Scope and current confirmed facts

Repository: https://github.com/FabinGurung/JP_Research-and-Development
Canonical single LaTeX controller: `controls/latex/tower.json` (v2.1.0).
One inherited base style: `controls/latex/template/pumlsc-shared.sty` and complete PU source-rule inventory `controls/latex/pu-format-parity-audit.json` (144/144 identifiers, **not 144 PDF-certified implementations**).
Researcher: `RSH-010` / `safal-dawadi`.
Q1 B: selected latest Safal manuscript version = v1.9 **reconciled Local Library seq15**, not October v1.2 Midterm, and NOT the first-uploaded v1.9 bytes.
Q2 A: PRE/POST by Git SHAs; major accepted release annotated tags only; no routine branches.
Q3 A: admit accurate manuscript `.tex`/`.bib` to R&D Git when real source recovered and verified; derived PDFs live as versioned Drive objects.
A7 global registry routes only; no competing A7 LaTeX template.

### Live source pointers

- PU v1.13 original: https://docs.google.com/document/d/1FjbNdNN_Fb_tKoapaYHW2jLoEF9lqxrYPYrCwTi87Ys/edit
- Thesis v1.23 control: https://docs.google.com/document/d/1jc6WIqXbAixAYYndeB2Idw59fAzjBbnDKlq49THeu_A/edit
- Safal source manifest: https://docs.google.com/document/d/1h-pw7TY9hVWHRfolJGvQpnXSprqdaen9fMUnIH2vwlQ/edit
- Safal project root: https://drive.google.com/drive/folders/1iMAzOXrs-9xivI25I2TS9Kd5afpY8MeP
- Safal Local Library: https://docs.google.com/spreadsheets/d/10g8-tr417XltYDbk2yItEZjrJ_2xdT7pbPlJgUI8MYo/edit (SyncState, LocalCatalog, ChangeLog, SyncDelivery)
- Latest target reported source SHA-256: `9c7bb25b84bd4a85aea85f137fdd8d080ab85c8fa18622a6d1ad9386d8f585bd`
- Latest target reported PDF SHA-256: `3d07e4a879f912b0b1d84e0e65c817e22166bd4f7e4be5c10c6525e43e58878a`
- First v1.9 source ZIP `1mgJ-_-Jc-z4XionxbjfpD9zinynSor9c` and PDF `1R9lRxDfgrvB1-s-o4-Y7GuN56zeD5itb` are **older first-uploaded bytes**, for provenance only; Local seq15 states same-ID mirror refresh pending.
- Safal source admission remains HOLD; Main Library seq15 acknowledgement has not been established (Local seq15 / reported Main cursor5; historic registry ack is only seq2).

## Next-chat execution contract

1. Fresh-read latest live GitHub main, R&D canonical tower and shared `.sty`. Fresh-read the PU v1.13 and Thesis v1.23 Drive originals and Safal project manifest, Local seq15, discussion/supervisor sources and exact Drive assets.
2. PRE = exact current Git main commit SHA and Drive IDs/hashes, no additional snapshot branch. Never overwrite original Drive artifacts, rename old baselines or create empty source files to feign completeness.
3. Search Safal's actual verified reconciled seq15 source bytes and PDF; try current Drive folder, governed archives, prior exact source/checkpoints, mounted files and tools. **Only accept target bytes if recomputed sha256 matches reported latest seq15 hash** or if a newly approved discrepancy reconciliation records exactly why/how changed and who approved. Retain older first-uploaded v1.9 separately. If verified current bytes are inaccessible, mark BLOCKER and do not claim v1.9 exact import.
4. Recover exact source tree and current chapter/bibliography/assets without fabricating researcher findings, observation counts, signatures, citations or results. Commit admitted textual source in `researchers/safal-dawadi/latex/manuscript/` and project metadata, never a copy of the shared template. Enforce `\\usepackage{pumlsc-shared}` in the manuscript; keep researcher-specific exceptions indexed in `controls/latex/extension-registry.json`.
5. Resolve conflicts using official PU guide > original official PU sample > explicit approved user decisions > approved technical evidence for formatting. Thesis source governance controls science/manifest/build provenance. R&D `tower.json` alone owns active shared implementation. Build out missing parity clauses centrally; all 144 source IDs are accounted for in audit but not all implemented/certified.
6. Linux setup if available (no invented installed tools): `sudo apt-get update && sudo apt-get install -y git python3 texlive-xetex texlive-latex-extra texlive-fonts-recommended texlive-bibtex-extra biber poppler-utils fontconfig fonts-croscore`. Check `xelatex --version`, `biber --version`, `fc-match "Times New Roman"`, `pdffonts -v`.
7. Verify `python3 scripts/validate_repo.py` and `python3 scripts/latex/safal_build.py --mode check`. The latter returning SOURCE_GATE=HOLD **does not mean ready**; after exact source admission and evidence, update source reconciliation/public Git/source admission gates to VERIFIED with traceable proof.
8. Attempt `python3 scripts/latex/safal_build.py --mode preview --output-dir /tmp/safal-v19-review` to build an explicitly Tinos-font non-production PDF **only after admitted source exists**. Preview uses central template and XeLaTeX/Biber/XeLaTeX/XeLaTeX, renders all pages and writes build-manifest.json.
9. If a licensed exact Times New Roman environment is genuinely available and font/asset/source/QA gates are all verified, attempt `python3 scripts/latex/safal_build.py --mode compile --output-dir /tmp/safal-v19-tnr-review`. Never mark FINAL/SUBMISSION based only on compiler success. Validate all 144 applicable university requirements, visually inspect every page, report figures/citations/warnings, preserve source/readback hashes.
10. For any global formatting fix, append central `RD-LTX-CHG-101+` proposal and update same shared `.sty` after regression checks. Project-only differences require recorded reason and extension, never duplicated base.
11. After source/build QA, commit Git changes non-force (PRE/POST) and read back changed files and workflow results; no new snapshot branches. Use annotated Git tag only after accepting a major release and actual tag capability; do not invent tag creation.
12. Store versioned PDF and QA artifacts in approved Safal Google Drive project if the publishing gate and write capability are available; provider readback and hashes required. Do not automatically push Local seq15 to A9 Main or claim supervisor approval.

### Linux caveat

The central template has a strict exact-Times-New-Roman production default; `--mode preview` explicitly injects an ephemeral `\\PUPreviewTinosFont` macro selecting Tinos. On machines without a licensed installed/registered Times New Roman, production compile **must remain blocked**; Tinos PDF is only a review preview. The GitHub Actions Safal workflow is currently a source-check job, **not** a PDF build service or Drive publisher.

### Completion contract

Report exact version/hash of source admitted, source commit and ref, PDF page count, SHA256, font list and embedding, QA and visual review status, public Git source links, Google Drive compiled artifact links/provider IDs where created, and unresolved scientific/approval/A9 synchronization gates. Distinguish TECHNICAL_PREVIEW from PRODUCTION_CERTIFIED. No false success.
