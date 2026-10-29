# Nabin Bista — full-document technical QA, SEQ049 Build 02

**Researched and checked 2026-10-29. No scientific LATEX_SEQ050 release.** This is a complete technical parity build of the existing September 2026 manuscript, not a revised six-block study.

- Current PDF: [stable SEQ049](https://drive.google.com/file/d/199DQW3Qan-jOpkO2PL3v-uKI_qJ6lu93/view)
- New independently compiled PDF: [69-page QA Build 02](https://drive.google.com/file/d/1_FHsrt9FlhYhn2dBy0Ptq24HLqDCbGjQ/view)
- [Complete source + QA ZIP](https://drive.google.com/file/d/1cWquSDwDglFjBCdVKbjsdKk9BgfVW8lJ/view) · [Dedicated Drive QA folder](https://drive.google.com/drive/folders/1suykLbQ3b2u1cHY-k3G7q7mRDzgDdI5_)
- [Machine QA record](seq049-fullqa-build02-20261029.json) · [Reusable PDF verifier](../tools/verify_pdf_parity.py)

## Actual tests
1. ZIP integrity and 238 original entries: PASS; new package adds two QA files without modifying the originals.
2. Two independent `pdflatex` passes with historic `main.bbl`: PASS, 69 A4 pages. Full PDF text is identical to CURRENT.
3. Full 69-page rendered pixel comparison at 72 DPI: PASS, 0 mismatched pages. All 69 page dimensions match.
4. Provider PDF was downloaded again after upload. An embedded **Content Credentials** attachment increases the provider PDF to 6,828,071 bytes versus locally compiled 6,727,771; all 69 visible pages and text still match.
5. Clean `bibtex8` regeneration was tested: command works, but drops uncited historical `dongol2020` entry, resulting in 20 items versus 21 in the preserved original main.bbl. This is a real scholarly/bibliography cleanup HOLD. The final QA PDF intentionally uses the preserved bibliography to avoid silent renumbering.
6. No source text, figures, dates, examiner names, or CURRENT PDF bytes were changed by this QA build.

**Release governance:** The six-block submission is not authenticated against the earlier single-prototype thesis. Do not call this LATEX_SEQ050, publish new numerical claims, or overwrite the permanent CURRENT PDF on a technical equivalence test. CI checks of source/website are not scientific validation.
