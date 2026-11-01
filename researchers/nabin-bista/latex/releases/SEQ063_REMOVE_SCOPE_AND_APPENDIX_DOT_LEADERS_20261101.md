# Nabin Bista — LATEX_SEQ063 (surgical manuscript correction)

Parent: **LATEX_SEQ062**. No new model, analysis, figure, table, claim, source data, bibliography, chapter or LaTeX template changes.

## Exactly two manuscript edits
1. `25_conclusionandrecommendation.tex`: remove **5.3 Scope of the Study** and its paragraph. Both **5.1 Conclusions** and **5.2 Recommendations** remain word-for-word unchanged.
2. `15_listofappendice.tex`: replace the ineffective `\\cftapplineleader` declaration with the list-entry control `\\cftappxleader`, set to `\\hfill`, eliminating the dots without changing the titles/page numbers.

## A7 permanent Drive source IDs (retained)
- PDF: https://drive.google.com/file/d/13beLy7N55TkgmMY1dzRpuK9hutmKFtjO/view (94 pages; SHA-256 `35599a4809490d249dcb153613d34f52e1b915fb1006111f71850568ab355ee9`)
- Source ZIP: https://drive.google.com/file/d/1XrUsz38STZ_2dliEOnxyNjlioYckuuKx/view (345 files; SHA-256 `36b2118bf489a8af71ea879de632cfa3fe918967de15e513910cfbeefbecbf8f`)
- Native Google Doc: https://docs.google.com/document/d/1AYv3p4rkL1XjvSfa1iiTmu0AqjdxZXEeQKXhiVvM6Qg/edit — unchanged historical content; not aligned with SEQ063.

## 000009 PRE/POST audit and recovery
- **SEQ062 PRE:** [PDF](https://drive.google.com/file/d/17mlDDX7BoRAMT6ETu7EUblhyIpZFNQhG/view), [ZIP](https://drive.google.com/file/d/1AsamapKSASfOcyH5y_ByIU8oj7IOHhVF/view), [native Doc](https://docs.google.com/document/d/18m-myq9aP4iMTceJc5QJrGAd8W3wh5_0fXkOp68SW4c/edit).
- **SEQ063 POST:** [PDF](https://drive.google.com/file/d/1JVp7FcthdXmTCoMhmCvTy_hOCw69TKrm/view), [ZIP](https://drive.google.com/file/d/16LGk_bX9mkmx0Q3rMXKVwRSlCC4xOr-Z/view), [QA JSON](https://drive.google.com/file/d/1etGCeXfELxE-QIstBWoNcmHq3yjqummL/view).
- Restore by replacing bytes in the SAME permanent live Drive IDs from the chosen PRE snapshot and creating a new numbered corrective sequence. Never delete PRE or POST.

## QA evidence and limits
- XeLaTeX compiled successfully for three clean passes after repairing one interrupted temporary build. Final PDF = 94 A4 pages, embedded genuine Times New Roman, no final-pass warnings.
- Rendered List of Appendices inspected visually: **no dot leaders**, Appendix 1 and Appendix 2 names and page numbers intact (physical PDF page 19).
- Search verified no section 5.3 in compiled document and chapter source.
- ZIP integrity passed. **Zero inherited source entries missing**, zero scientific image/data files changed. Only the two specified `.tex` source files have content differences (plus generated build files and SEQ063 manifest).
- Native Google Doc not updated under this task scope; exact Docs/PDF parity is not certified.
