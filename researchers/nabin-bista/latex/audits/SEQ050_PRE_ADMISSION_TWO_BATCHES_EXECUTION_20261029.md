# Nabin Bista — two-batch independent technical preview (2026-10-29)

**Researcher RSH-003. No scientific LATEX_SEQ050, no academic PDF release.**

## Actual executed controls
- Exact first-batch ZIP checksum checked, 67 XLSX workbooks/228 sheet labels/36 embedded XLSX chart objects inventoried, and 24 modal block/soil values parsed through the spreadsheet reader. One Block2 hard-soil sheet uses a shifted table; T1 read from D6 = 0.594 s.
- Researcher batch2 DOCX Table3.1 (six block geometries), Table3.4 (18 block/soil rows) transcribed; **seven** Block5 spring cells remain censored as `########`; no invented inputs.
- Same architectural plan SHA across both October batches; Blocks1–4 PNGs are exact duplicates, while Blocks5–6 differ. Both older/newer variants retained in the PRIVATE source custody ZIP.
- Standalone 15-page LaTeX evidence annex compiled from a new scoped `main.tex`, with source plan page6, 3D block views pages7–12, B5/B6 comparisons pages13–14, and tabular/modal source figures. Build log: three pdflatex passes, no overfull/fatal errors; 11 raster objects plus plan PDF vector content, 14 expected anchors checked.
- Candidate PDF local SHA256 `e2e6262c67f14e488c7f48ecbc2a6e065a3eb3042b82da538aa05cf0250d3052`, 6,538,149 bytes. Private complete carrier ZIP SHA at UPLOAD `ec47d6e94835017f746866785a8ae5914efb9380e1159970d63c06dc617e4217`, 77,711,839 bytes. Drive provider ID/size/parent verified, provider byte SHA not independently rehashed.
- The complete original source files and image binaries are **in Nabin's dedicated private Drive**, not public Git. See Discussion Google Doc Chapter 15 (same permanent ID) and Scientific Audit v0.6 for exact links and the candidate `compiled_preview_inclusion_ledger.json`.

## Safety
This preview is **not** the LATEX_SEQ050 thesis and does not contain all 36 source workbook charts rendered into approved Chapter4 figures. Nine source identity conflicts, Block5 masked springs, ETABS model identity, possible four-vs-five fragility threshold mismatch, waveform direction/provenance and legacy bibliography issues remain. None of the original scientific LATEX_SEQ049 manuscript, shared style, or CURRENT Drive ID was changed.

`tools/check_candidate_inclusion.py` checks mapped PDF pages and fails closed for academic mode while the manifest retains unresolved release conditions. Passing a CI repository check must not be presented as approval of experimental data or engineering science.

Next tracked issues: [#51](https://github.com/FabinGurung/JP_Research-and-Development/issues/51), [#52](https://github.com/FabinGurung/JP_Research-and-Development/issues/52), [#53](https://github.com/FabinGurung/JP_Research-and-Development/issues/53).
