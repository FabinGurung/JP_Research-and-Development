# Saugat Paneru — 3× cover logo / current-month LaTeX template QA
**Date:** 2026-10-20 NPT | **Scope:** RSH-002 format-only | **Change:** RD-LTX-CHG-107 | **Status:** LOCAL_RENDER_QA_PASS / RELEASE_HOLD

## Authority and source
- Accepted scientific CURRENT: **CP114 / LATEX-SEQ-028**, 115 A4 pages. [Original PDF](https://drive.google.com/file/d/1aFVnwamHhp2Xpjmg10UfMPBwK031HMTh/view); [frozen original source ZIP](https://drive.google.com/file/d/1yL3G-EUGA32FDBhkdImXk9NManfW_vyA/view).
- Reused existing Saugat prior 115-page candidate and registered CP114 typography parity adapter from [RD-LTX-CHG-106](CP114_SHARED_TEMPLATE_TOC_PARITY_20261019.md).
- One canonical shared stylesheet: `controls/latex/template/pumlsc-shared.sty` upgraded v2.3 → **v2.4**, with *opt-in* logo scaling and `\PUCurrentMonthYear` macro.
- Researcher-scoped adapter `researchers/saugat-paneru/latex/extensions/saugat_project_adapter.sty` invokes `\PUScaledCoverLogo{\PULogoFile}`.
- Researcher project config sets `\PUCoverLogoScale{3.0}` and `\PUSubmissionDate{\PUCurrentMonthYear}`.
- Saugat build script sets `TZ=Asia/Kathmandu` to resolve build-month/year at Nepali month boundaries.
- Scientific `.tex` chapter modules and `references.bib` were not changed. Historical CP114 artefacts remain unchanged.

## Exact-font local render QA
- Local source reconstructed from frozen CP114 ZIP and Git shared-template/adapter semantics, with private licensed Times New Roman. Font binaries were **not** embedded in source package or Git (fonts are embedded only as PDF subsets).
- Full XeLaTeX → Biber → XeLaTeX stabilization succeeded; **115 pages A4**; 115/115 pages independently raster-rendered.
- Main fonts are exact Times New Roman / Times New Roman Bold.
- Cover image originally 115.203 × 65.830 pt, now 345.610 × 197.492 pt. Scale x=**3.000023**, y=**3.000023**, original aspect preserved.
- Cover and title page date: **October, 2026**. Recompilation automatically recomputes month + year.
- Comparing against prior migrated 115-page PDF, **115/115 page extracted texts are identical after substituting September, 2026 ↔ October, 2026**. The logo is the intended visible pixel/layout change.
- New QA PDF size: **55,177,712 bytes**; SHA-256 **`5bbe2bcf006f16f823e796ca9c6722c122de69c27cec7955803d98b07b6d3428`**.
- Standalone source QA ZIP containing 187 archived files (excluding licensed font binaries) SHA-256 **`52200665d4340070c83384325beeea690f4cd67898bf9d8c86754019123e25c8`**.
- This local source snapshot is a reconstructable packaging of frozen CP114 input and equivalent Git macro definitions; a Git-provider build-from-exact-checked-out-bytes is **not separately certified**.

## Governance
- The original CP114 PDF and source ZIP retain their Drive IDs, hashes, and scientific authority.
- The new PDF and source ZIP are local QA artifacts; **not uploaded/read back from governed Drive candidate storage** in this run.
- University-wide 144-rule compliance remains `HOLD`; no other researcher's PDF formatting is modified.
- No Git release/tag or thesis production promotion asserted. Review and admit any release only after Drive provider readback and format acceptance.
