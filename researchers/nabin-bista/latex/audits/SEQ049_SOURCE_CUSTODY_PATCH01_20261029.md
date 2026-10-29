# Nabin Bista (RSH-003) — LATEX_SEQ049 technical source-custody patch 01 (29 Oct 2026)
This **is not LATEX_SEQ050** and does not incorporate the October six-block workbook or hospital plan into the September 2026 thesis.

## What changed
The prior corrected source ZIP had 235 original entries and omitted two referenced historical PDF figures. A recovered, tested intermediate source added those two figures without changing any original entry. This new patch ZIP preserves all 237 recovered-source entries and adds a `SEQ049_SOURCE_REPAIR_PATCH01_READ_FIRST.txt` receipt; original LaTeX `.tex`, `.bib` and `main.bbl` bytes remain identical to SEQ049.

**Drive technical-QA folder:** https://drive.google.com/drive/folders/1tTPJXYJjDYciobn3MwqdnmmPdkDJHCsM

**Complete source patch ZIP:** https://drive.google.com/file/d/1JHDhBD8-UgEOMPz-IC_-BUJ7gizjtJpD/view (24,801,910 bytes; local SHA-256 b3509dc2113064a533246232b6bd78927209a7b123110e04d8ccb8bfaaf10e5a).

**Recompiled PDF:** https://drive.google.com/file/d/172k62riI9rNF2sYvwhq5yBOSX-d6z1Xc/view (6,435,967 bytes; local SHA-256 c7d61ea54bbdc56e34517ff3fed19af18baf29db537f3a12740c9f7dbf6faa02).

## QA
- Independently XeLaTeX compiled in two passes with the historical `main.bbl`, with **69 physical PDF pages** and visible References on physical PDF pages 58–60.
- Comparison to the permanent CURRENT source PDF: 66/69 pages text-identical after NFKC/whitespace normalization; math-symbol extraction differences on pages 33, 34, 36. Pixel comparison showed subpixel rendering differences; never claim the two binary PDFs or renders are exactly equal.
- ZIP integrity tested and all 237 pre-patch entries byte-identical. Original files remain untouched; Drive provider metadata readback confirmed newly generated upload IDs, sizes and dedicated technical-QA folder.
- No independent BibTeX regeneration (BibTeX program absent); the complete corrected historical `main.bbl` remained present. Do not claim a fully fresh bibliography generation.
- Original CURRENT LATEX_SEQ049 PDF remains at https://drive.google.com/file/d/199DQW3Qan-jOpkO2PL3v-uKI_qJ6lu93/view with original title and Drive file ID. Do not replace or claim the separate rebuilt QA PDF as CURRENT.

## Scientific release gate
The October 2026 six-block evidence remains unresolved on model identity, damage-state mapping and waveform provenance. The September 2026 academic manuscript cannot silently absorb post-date data. Keep scientific LATEX_SEQ050 on HOLD until explicit bounded source admission, new date authorization (if relevant) and all-page PDF QA. Preserve Git history, source/evidence Drive IDs, A7 PRE/POST snapshots and previous releases.
