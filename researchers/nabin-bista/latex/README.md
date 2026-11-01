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


## Working thesis release — LATEX_SEQ060 (2026-11-01)

The latest working **compiled PDF and complete source ZIP** are registered as [LATEX_SEQ060](versions/seq060.json), child of SEQ059, with numbered PRE/POST restoration. The [CURRENT pointer](versions/CURRENT.json) preserves stable live Drive IDs. Scope: four Nabin Block 1–2 appendix displacement/drift plots and corresponding captions; no other scientific changes. The native Google Doc is still at SEQ059 and Blocks 3–6 raster plot labels remain on hold; consult the [internal release audit](releases/SEQ060_BLOCK1_BLOCK2_PROFILE_CLEANUP_20261101.md). Previously accepted scientific versions remain separately governed.


## New working manuscript LATEX_SEQ061 (2026-11-01)

[Version 061](versions/seq061.json) is the latest working PDF/LaTeX, reusing all permanent Drive IDs and preserving sequence 060 under numbered 000007 PRE snapshots. Four source files were edited in place: single-page Abstract, removal of duplicate Chapter 3 plan, six 2D blocks paired two per page, and 36 response/fragility plots rehomed under Chapter 4. Global shared format v2.6.3 applies two-line chapter headings without chapter page numbers in TOC. [Release and recovery](releases/SEQ061_CHAPTER_TOC_AND_FIGURE_PLACEMENT_20261101.md). Native Google Doc exact parity remains pending. No new numerical scientific values were introduced.


## Latest working LaTeX thesis: LATEX_SEQ062 (2026-11-01)

[SEQ062 release register](versions/seq062.json) preserves the same live Drive PDF/ZIP IDs, archived SEQ061 PRE 000008 and SEQ062 POST 000008. The scoped revision enlarges Appendix 2 Figure 2.1, removes the empty plates list, consolidates the specific objectives to three, makes the abstract one page, and compares the six-block findings carefully against two DOI studies. No original image/data source was modified. Native Google Doc still requires synchronization and visual parity. [Release/QA notes](releases/SEQ062_CONCISE_ABSTRACT_OBJECTIVES_AND_DOI_COMPARISON_20261101.md).


## Current working thesis: LATEX_SEQ064 (supervisor-feedback revision)

The complete [SEQ064 version record](versions/seq064.json) and [PRE/POST restoration note](releases/SEQ064_SUPERVISOR_CORRECTION_GOVERNED_20261101.md) describe the same-live-ID PDF and source ZIP updates, six-block fragility layout and source-backed editorial corrections. Scientific engineering verification and updated native Google Doc parity remain open; this working revision must not be treated as final scientific approval.
