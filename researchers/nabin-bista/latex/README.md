# Nabin Bista · LaTeX source lane (RSH-003)

**Researcher-scoped source admission candidate for the existing 69-page `LATEX_SEQ049` PDF.** This folder adds text/code to Git; no other researcher file, existing template, or original Google Drive artifact is replaced.

- [Source/PDF/legacy-Drive manifest](source-and-drive-manifest.json) · [Current thesis PDF](https://drive.google.com/file/d/199DQW3Qan-jOpkO2PL3v-uKI_qJ6lu93/view) · [Corrected reproducible ZIP](https://drive.google.com/file/d/1noTWs5mOFjn10-i3rVSBbWlex1C12CJB/view)
- `manuscript/main_SEQ049_original.tex` (byte-equivalent to the ZIP's `main.tex`) and its subfiles plus `27_reference.bib` are direct UTF-8 extracts from the corrected source ZIP, not reformatted or scientifically rewritten for Git.
- `legacy-tools/` contains the source-package Python scripts for historical reproducibility. They are **not invoked automatically**; some depend on data/figures stored only in Drive.
- The repository's **single latest shared LaTeX authority** is [the tower](../../../controls/latex/tower.json) and [shared style](../../../controls/latex/template/pumlsc-shared.sty). This imported `main.tex` retains its legacy style exactly. Switching to the global style requires a separately controlled formatting change, independent render and 69-page QA; it has **not been silently forced**.
- Figures, spreadsheets, original research data, compiled PDFs, personal/private evidence and font binaries were **not imported into this public repository**. Therefore **Git source alone is not a complete standalone production build**; use the exact Drive ZIP with its source provenance for reconstruction.
- Source validation through GitHub Actions is separate from actual PDF compilation, university formatting parity, scientific approval and Pages deployment. Production Pages builds from `main` only.

Old Drive links and legacy researcher branches remain valid and preserved; see the append-only pointer manifest for both new and former identities.

### Source-admission gate

The corrected Drive archive's `main.tex` is copied exactly to `manuscript/main_SEQ049_original.tex` so Git can preserve the original academic source without treating the legacy file as a shared-style-admitted production entrypoint. The repository's universal source validator requires every **active `main.tex`** to import `pumlsc-shared`. A future authorized template conversion should create the active `main.tex` and validate the full 69-page layout; do not edit the historical original to make the source validator green. The Drive ZIP retains the exact original filename and its full external assets.

## 2026-10-29 source custody and next-release gate

The SEQ049 Drive ZIP omits two referenced PDF figures, now recovered by exact SHA from the preserved SEQ046 ZIP. An additive 237-entry source ZIP tested locally to 69 pages with the existing main.bbl; no Drive upload or new PDF release occurred. See SEQ049_SOURCE_CUSTODY_QA.json and NEXT_RELEASE_READ_FIRST.md. Historical source uses BibTeX (not the shared Biber default); fresh BibTeX compilation is still unverified in this runtime.

## 2026-10-29 Submission02: six-block dimensions, springs and updated model figures

The new original DOCX + 7z are preserved in Nabin's Drive and indexed as a second October submission. The earlier 67-workbook plots ZIP and 495KB plan are NOT in the 69-page LATEX_SEQ049 manuscript, and the new 7z's Block 5/6 images are changed from their prior variants. Source custody, duplicates, and obscured Block5 spring cells are explicit HOLDs. [Read full two-batch admission and full-figure completeness prompt](prompts/SEQ050_ALL_OCTOBER_SUBMISSIONS_SOURCE_TO_PDF_READ_FIRST.md). Old source branches and links remain intact. The historical status sections above remain as event-time audit history; the latest Build02 upload and 69-page QA are documented in `audits/SEQ049_FULLQA_BUILD02_READ_FIRST.md`.


## Current working LaTeX release (version-control correction, 2026-11-01)

The already completed six-2D-figure and cover-logo manuscript state is **LATEX_SEQ059**, not SEQ058. PRE remains SEQ058; POST is SEQ059; live Google Drive IDs are unchanged. See [version pointer](versions/CURRENT.json) and [immutable SEQ059 version record](versions/seq059.json). Prior history above is preserved as historical evidence; source quality/approval gates remain separate.
