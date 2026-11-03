# Nabin Bista — LATEX_SEQ067

2 November 2026, Asia/Kathmandu. Figure typography and layout revision of the verified live SEQ066 source. This is a working research manuscript, not scientific approval.

## What changed

65 existing numeric plots and two explanatory diagrams now use exact Times New Roman at 12 pt. Native plot PDF sizes match LaTeX inclusion sizes, avoiding font shrinkage. The four original Block 1 support panels remain Figure 4.30, with a fifth panel comparing all sixteen existing damage-state/support curves. Colour denotes IO/LS/CP/C, line style denotes support; axes and 0.2 grid spacing match. Existing workbook probabilities are reproduced without a new fit. Waveform and spectrum plots preserve their coloured plotted pixels and replace text/axes only. All original 222 binary assets, including 15 original workbook/DOCX/ZIP records, are byte-identical to SEQ066.

The highlighted figures were present in SEQ066 (PDF pages 55, 70 and 73). They were not absent. This revision retains their scientific positions and numbering. The PDF has 120 A4 pages and 88 numbered figures.

## Explicit annotation exception

Seven source plan figures (3.3–3.8 and A2.1) retain their original CAD annotation geometry and sizes. The six block plans contain outlined glyphs; the whole-hospital plan has 840 dense annotation spans. They are not certified as 12 pt Times New Roman. Their conversion requires a faithful technical-drawing redraw with verified labels, without changing dimensions. No universal all-figure font-compliance claim is made.

## Build and figure inputs

Run `bash build_seq067.sh` after installing the owner's exact Times New Roman fonts. All active figure PDFs are inside `figures/seq067/`. PNG copies are included. No Google Doc is required or generated. The compiled thesis is supplied separately at the permanent PDF Drive ID; `main.pdf` is excluded from this source ZIP to keep the upload within the provider limit. All compilation inputs and original assets are retained. `scripts/finish_seq067.py` reproduces charts and diagrams from the packaged sources and preserves the existing numerical method; it requires numpy, scipy, matplotlib, Pillow, PyMuPDF and tesseract.

## A7 preservation and restore

PRE source: https://drive.google.com/file/d/1ik62d9d28EtiK93LLzK7UPzlv6Ref2Hy/view
PRE PDF: https://drive.google.com/file/d/1dgflS_W2ycIMhgXzXFGflhMQbZSWjghq/view
Archive folder: https://drive.google.com/drive/folders/1yb6ejHj-D2IhJAk2qh2WePYKNfmA8mz9
Live source ID: 1XrUsz38STZ_2dliEOnxyNjlioYckuuKx
Live PDF ID: 13beLy7N55TkgmMY1dzRpuK9hutmKFtjO

To restore SEQ066, copy the exact bytes from the 000013 PRE source/PDF into those same permanent IDs, restore their SEQ066 titles, and append a restoration entry. Do not change existing sealed PRE/POST records. This source lane follows the existing SEQ066 Git lane. Inherited shared-style CI and scientific validation holds remain open.
