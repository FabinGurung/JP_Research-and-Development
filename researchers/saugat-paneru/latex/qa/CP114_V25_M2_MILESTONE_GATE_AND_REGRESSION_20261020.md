# Saugat CP114 — v2.5 formatting-QA milestone gate / experiment log
**Record:** RSH-002 / QA-MG2-20261020 / PR #32  
**State:** triage evidence committed; Milestone 2 not yet qualified for final release  
**Scientific current:** CP114 unchanged  
**Formatted production CURRENT:** v2.4 [PDF](https://drive.google.com/file/d/1tuXDpv1eP9bPqVbLfqimmRMQTQo8Eqvg/view)

## Completed and reproducible
- [x] One Drive file named `CURRENT_CHECKPOINT` now identifies v2.4 production; original CP114 scientific checkpoint preserved under historical name. Git change in merged PR #31.
- [x] All 144 original university control entries enumerated; missing numeric `PU-FMT-076` remains source-native, not fabricated.
- [x] v2.5-RC1 fresh PDF and complete 214-file source ZIP available in [Drive QA folder](https://drive.google.com/drive/folders/1hrR8zwIB7gCa5bPY-ALhKUeJOEeOZsux) with verified SHA256 roundtrip.
- [x] Strict RC1 compiles 115 A4 pages, 81 embedded image occurrences; XeLaTeX/Biber stabilization QA previously passed without final overfull boxes.
- [x] 5 remaining line-end hyphen breaks individually identified. They occur at authored compounds, not newly inserted hyphenation of originally unhyphenated words:
  - p35 `MRT/RUD-designed`: source `chapters/chapter2_literature_review.tex` line 125 includes an explicit `\\allowbreak{}`.
  - p51 `X- and`: source `generated/tables/modal_extraction_fields.tex` line 11 uses an already-hyphenated directional qualifier.
  - p72 `displacement-reversing`: source `chapters/chapter4_results_discussion.tex` line 310 includes `\\allowbreak{}`.
  - p80–81 `performance-point`: `chapters/chapter4_results_discussion.tex` line 425 and elsewhere explicitly include `\\allowbreak{}`.
- [x] Font-size screening across the 115-page PDF isolated **15** pages with under-10-point text in original chart/plan assets: **42, 43, 57, 58, 59, 65, 66, 73–79, 87**. Screening is not a declaration that all subscript glyphs or embedded-source labels are non-compliant.
- [x] Direct page renders of pp42, 57, 65, 73, 87 inspected. Page 65 has genuinely tiny multipanel legends and embedded source labels; these merit source-asset correction.

## Regression experiment rejected, NOT committed to manuscript
A formatting-only **zero-line-break** experiment grouped 5 compound term families using `\\mbox{}`, including the already authored `\\allowbreak{}` constructs, without editing scientific text or numerical values. Independent XeLaTeX/Biber 4-pass compile succeeded. Converter emitted a **116-page PDF**, with **0** detected line-end hyphen breaks and **81** image occurrences, but introduced **one 1.32507pt overfull hbox** (the literature comparison table) and **321 underfull hbox** warnings. The prior 115-page RC1 thus remains the governed candidate; **zero-hyphen trial failed regression** and must not be promoted. Trial source/PDF retained only locally, not copied into approved Git manuscript.

## Remaining milestone gates and required repairs
1. **PU-FMT-039:** Recover traceable figure-generation sources for charts with undersized text. Where available, regenerate from the *same admitted data* with legible fonts and check the numerical curves/axes/legend against immutable authority assets. If original source/data is missing, stop; document explicit exception, do not redraw by estimation.
2. **PU-FMT-007:** Decide whether breaking an *already-hyphenated* compound at its explicit hyphen is permissible. The 182 ordinary split words from v2.4 are eliminated in RC1. No broad `\\mbox{}` rewrite may be admitted without a no-overflow pagination gate.
3. **PU-FMT-016:** Preserve user-requested 3x logo as documented source-level exception; do not report strict conformity with original 1.6in logo slot.
4. **115-page final visual and structural QA:** every final page, captions/subfigures, math glyphs, margins, lists, blank/orphan pages, figure readability, page transitions, remaining underfull warnings. A different justified total page count is possible only with evidence of necessary legibility improvement and a full regression pass, not a silent pagination change.
5. **144-rule evidence audit:** resolve 76 partial and 22 unverified statuses with applicability-specific evidence; never mark 144/144 approved without actual evidence. This includes documentation/workflow rules not necessarily automated by a LaTeX class.
6. **Release:** Once corrected source + independently recompiled PDF pass all applicable gates, merge a new controlled version with CI; update Drive binary deliverables and canonical `CURRENT_CHECKPOINT` with SHA256 readbacks. Keep CP114's science frozen.

**Next actual milestone:** `M2 — V2.5 FORMAT_QA_FROZEN` once the above format blockers are closed with verified evidence. Date is *gate-driven*, not an invented schedule. `M3 — V2.5 PRODUCTION_RELEASED` follows merge, documented review/approval, Drive upload, checksum/readback and stable CURRENT update. 
