# Nabin Bista — LATEX_SEQ057 revision R1

This directory contains 32 versioned LaTeX and BibTeX source files for the 95-page review manuscript. Private research binaries and complete source ZIP remain in Nabin's governed Google Drive, and SEQ056 / historical CURRENT remain preserved.

## Publication artifacts
- [PDF review](https://drive.google.com/file/d/13beLy7N55TkgmMY1dzRpuK9hutmKFtjO/view)
- [Complete original-source ZIP](https://drive.google.com/file/d/1XrUsz38STZ_2dliEOnxyNjlioYckuuKx/view)
- [Native editable Google Doc review](https://docs.google.com/document/d/1AYv3p4rkL1XjvSfa1iiTmu0AqjdxZXEeQKXhiVvM6Qg/edit)

## Fetch the one canonical shared LaTeX template
R&D single style is [pumlsc-shared.sty](https://github.com/FabinGurung/JP_Research-and-Development/blob/main/controls/latex/template/pumlsc-shared.sty), v2.5.0 at commit d0a8c588d25edf11d1de104a07a21be1ab59ff7e.

    curl -fsSL https://raw.githubusercontent.com/FabinGurung/JP_Research-and-Development/d0a8c588d25edf11d1de104a07a21be1ab59ff7e/controls/latex/template/pumlsc-shared.sty -o /tmp/pumlsc-shared.sty

Source of truth is the single global style; do not fork a second copy. The historic R1 main.tex contains local typesetting logic and is **NOT YET FULLY PORTED** to loading the canonical style package. A later source migration and complete visual regression are required before claiming full style inheritance.

**Exact production font:** Times New Roman in the [owner-only cache](https://drive.google.com/drive/folders/1nf_nRgYbEXdA4xK7bhuA3tdgha8khvyv). Licensed font binaries must never be committed to Git or redistributed inside thesis ZIPs. The R1 PDF embeds exact Times New Roman.

The Google Doc contains native editable text and selected inline figures but has not passed exact tables/equations/figures/pagination comparison. Do not designate submission-ready. Researcher-approved scientific and visual QA is scheduled for a later run. Internal source/provenance records remain outside the student submission prose.
