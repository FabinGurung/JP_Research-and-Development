# Nabin Bista LATEX_SEQ078 — formatting-only release

Parent: LATEX_SEQ077. A7 event: 000021. Researcher: RSH-003.

## Authorized formatting differences from LATEX_SEQ077
- Table 3.2 compacted with 12-pt text and 0.92 table row stretch; six block records and all cells remain the same. All six slab entries and the bottom rule fit on thesis page 22.
- Conservative researcher-local float spacing applied; paired figures where legible. All 88 figure caption identifiers remain intact, with no changes to scientific plots or data. Reported placement: 35 pages with 2+ figures rather than 27; 113 pages, previously 120.
- Researcher-specific top margin 1.33 inches (33.782 mm), as requested. This DISAGREES with current registered PU-FMT-003 official margin 2.5 cm. It is a documented user exception, not a claim of Pokhara University approval or shared-style change.
- Figure A2.1 on a single A3 landscape sheet, enlarged to approximately 0.965 text height with safe trim; printed thesis page 77 due pagination after figure compaction, physical PDF page 98. Figure number, image content and caption unchanged.

## Reproduction
Use `bash build_seq078.sh` with XeLaTeX, BibTeX8 and the inherited `controls/latex/template/pumlsc-shared.sty` v2.6.4. Provide an authorized local installation of Times New Roman. No font files are distributed.

## Scientific boundary
No ETABS computations, values, results, citations, captions or scientific assertions were revised. Code QA does not establish scientific or University compliance. See `SEQ078_LOCAL_QA.json` for rendered checks and explicit conflict.

## Version control and restoration
GitHub R&D main owns versioned source; Google Drive owns the two permanent manuscript binary IDs. A7 000021 PRE archives preserve exact SEQ077 PDF and ZIP. The permanent IDs remain stable. Never overwrite the PRE or POST archives during subsequent revisions.
