# Nabin Bista — LATEX_SEQ064: scoped supervisor-review integration

## Version continuity
- **Parent:** LATEX_SEQ063, preserved as immutable `000010_PRE` prior to mutation.
- **Working revision:** LATEX_SEQ064; no change to the permanent PDF, LaTeX ZIP or native Google Doc Drive IDs.
- **Immutable `000010_POST`:** complete revised PDF and source ZIP plus restricted internal response and QA records.
- **Global LaTeX shared style:** owner repository main.tex continues using `pumlsc-shared.sty`. Owner scientific data/figures retained and no licensed font binaries are committed.

## Live Drive
- PDF (107 A4 pages, Times New Roman): https://drive.google.com/file/d/13beLy7N55TkgmMY1dzRpuK9hutmKFtjO/view
- Complete populated source ZIP: https://drive.google.com/file/d/1XrUsz38STZ_2dliEOnxyNjlioYckuuKx/view
- Native Google Doc: https://docs.google.com/document/d/1AYv3p4rkL1XjvSfa1iiTmu0AqjdxZXEeQKXhiVvM6Qg/edit — remains an **older** version; **not** PDF parity-certified.

## A7 restoration
- `000010_PRE` SEQ063: [PDF](https://drive.google.com/file/d/1mX8VSypj-YFSKMsS_fGvsrRZUUtQIQOF/view), [ZIP](https://drive.google.com/file/d/1hqfOMQfo-d0jxZ6FV0Xo8XhcvlUVEnGP/view), [native Doc](https://docs.google.com/document/d/1zOaxTt-jQtc-a7539JOwouxM-po9M1K-9iGW7ZZwUv4/edit).
- `000010_POST` SEQ064: [PDF](https://drive.google.com/file/d/1oHbk2wdrbeWqtGyo0qYZkiRdx5-mua5e/view), [ZIP](https://drive.google.com/file/d/1VP0XTXR2zG459sp8cPDHL5ne20GpWC6n/view), [QA](https://drive.google.com/file/d/1zDelqNvWFNfWdwUh7EcbTvjEzwpsdEe8/view), [review-response register](https://drive.google.com/file/d/1WNoNWlGdAoEmBdUPYLrwAdudL8zN6YXp/view).
- Restore with PRE bytes **into the permanent live IDs** and append a new numbered restoration entry; never delete the source archives.

## Manuscript changes
- Aligned thesis title across front matter, research objectives and questions to the six-block mid-size hospital case study.
- One-page abstract and quantitative conclusions; retained original numerical source values.
- Documented one verifiable Gazetas vertical spring hand-check and clarified soil support as a parametric comparison, with unit conventions.
- Removed three questionable reaction entries as uninterpreted measurements in Table 4.7; did not fabricate corrected ETABS results or silently rewrite source data.
- Retained all 24 original fragility illustrations in Appendix A3, with six four-support Chapter 4 composite panels.
- Updated appendix figure numbering, selected table captions, research-gap grammar and research prose.
- Three of 21 supervisor-review comments fully addressed, 12 partially, six require original model/code/evidence work. Scientific submission remains unapproved.

## Evidence and hold boundaries
- Final local XeLaTeX/BibTeX render: 107 pages, embedded exact Times New Roman, no unresolved references, no removed inherited files, no changed original .xlsx/.csv or figure image bytes, valid ZIP CRC.
- Explicit unresolved analytical checks: Table 4.7 ETABS re-export; six-component spring/footing reconstruction and bearing checks; spectrum/R factor/mass/drift amplification; base vs storey shear; block-level lognormal fragility fitting; nonlinear model checks, sensitivity and hospital-specific verification.
- This is a **working revision**, not evidence of newly executed ETABS analysis or full submission readiness.
- Public GitHub code and metadata **exclude the confidential supervisor review PDF**; its response is held in Drive.

## Reproducibility caveat
The published PDF was compiled from the populated Drive ZIP, which contains the inherited local source-compatible legacy preamble. The public GitHub `main.tex` deliberately retains the canonical shared-template inheritance and has not been independently recompiled to prove a binary-identical PDF. Do not claim exact GitHub/Drive render parity from source check CI alone.
