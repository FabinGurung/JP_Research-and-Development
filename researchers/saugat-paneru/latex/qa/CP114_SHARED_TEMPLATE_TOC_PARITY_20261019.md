# Saugat Paneru — CP114 shared-template contents parity QA
Date: 2026-10-19 (NPT) | Researcher: RSH-002 | Scope: FORMAT ONLY

**Status: LOCAL PDF QA PASS; DRIVE RELEASE / CURRENT PROMOTION NOT PERFORMED.**

## Verified authority
- Accepted CP114 PDF: Drive `1aFVnwamHhp2Xpjmg10UfMPBwK031HMTh`, 115 A4 pages, SHA-256 `55efba49159d1f5931d042f539c3f3efcd22df0684b1e565d27819a0a6c935cb`.
- Original CP114 source ZIP: Drive `1yL3G-EUGA32FDBhkdImXk9NManfW_vyA`, SHA-256 `3af05ae5647de3311ac2941c387d3513fe76a5d29e8d6b6aaae152fb1a653bef`.
- Previous Git-template QA PDF: Drive `1JbN0d-lOEMCgpFxyXKRj7FhNFeGpuuxr`, 116 A4 pages, SHA-256 `db134c2b4254fe84ea6aceff966620407b08b0f5f3d63487554ad6777a5565f8`.
- PRE Git main: `48a1d44f4835b8cade0e95be66a51fed353f4836`.

## Exact source tree files used in local build
- Main `a48a160a985bdab0ab24dfc21a9f24a862f0d891`.
- Canonical shared template `f6d8b8fba284603604358d50eed285f722b0c3a0` (**unchanged**).
- Researcher-specific adapter `1e73c5f80409743ada934a740322678f98db288f`.
- Compatibility extension `5d511f8c37eb757398004c9fe274a46fc0bf6881`.
- All binary figure assets sourced from frozen CP114 ZIP. Private licensed Times New Roman faces used locally only; **not committed or bundled**.

## Implemented correction
Original shared-template candidate added a preliminary-page spill by changing the TOC and other list typography. Applied only CP114-specific `tocloft` chapter leaders, font weights, spacing and list-heading macros in the registered `saugat_project_adapter.sty`, plus the Saugat appendix-list entry type; no global duplicate template and **no changes to scientific .tex or .bib**.

## New corrected local output
- Full XeLaTeX → Biber → XeLaTeX stabilization: 4 XeLaTeX passes; final build **115 A4 pages**.
- Final PDF SHA-256 `2f8c4566377df5af4efa23e4d2804ced8e415b9764f90c63f2e0003557f1ab59` (local candidate only).
- **115/115 rendered** with no renderer error, 81 embedded image objects, no text blocks crossing page bounds.
- Exact embedded Times New Roman detected in main body by `pdffonts`. Other embedded typefaces appear within originally supplied figures as in CP114.
- Text on preliminary pages 1–10: exactly equal to accepted CP114 on extraction. Pages 11–17 text similarity at least 99.69% except differing page-reference numbers; appendix pages 95–115 extracted text exactly equal.
- Body is source-identical to the CP114 admitted scientific subfiles; PDF page layout of floating figures/tables may differ owing to changed common heading/spacing defaults. PDF byte equivalence is **not asserted**.
- No logged fatal TeX errors, undefined citations/references, Biber warnings, overfull boxes or oversized floats.

## Explicit remaining gates
1. Push this adapter and records through GitHub CI, retain exact POST SHA and CI links.
2. Copy/upload the corrected 115-page candidate into governed Saugat Drive project, re-download/read back and verify SHA-256. Current local runtime file is **not yet a Drive release**.
3. Provide full-document visual approval and any required program/researcher authorization before promoting CURRENT.
4. The global shared PU 144-rule certification remains `HOLD`; a Saugat-specific 115-page parity fix does not certify all researchers.
5. Scientific evidence debt `DEBT-SAUGAT-001` remains open and is outside formatting migration scope.

No Git tag, GitHub release, Drive production promotion, nor CURRENT checkpoint change is asserted by this QA record.
