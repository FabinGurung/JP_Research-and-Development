> **2026-11-01 source and preview QA readback (not CURRENT):** Shared template v2.6.4 amendment PR #118 merged; numbered SEQ032 reservation PR #119 merged; Saugat researcher-only PR #120 draft, repository 4/4 source checks passed on initial source revision. Full private 251-file source candidate ZIP recreated from the 249-file parent, original 12 numeric CSV/XLSX inputs byte-identical. Tinos PREVIEW built with XeLaTeX+Biber: **115 A4 pages** with no overfull box, float-too-large, or unresolved-reference messages at the fourth and later pass. Figure 3.3 PDF p46 (Regular); 3.4 p47 (L/L1/L2/T/U in two columns); 3.5 p48 (Non-Parallel); all 8 original model PNGs shown as Figures 3.7–3.14 (PDF pp49–50); Table 4.4 p60 is 12pt in PDF text spans. PRE archive Drive ID `1_BGwgjyAFJHK0GKtYxdKJTguz5pjlS0V`. Saugat Drive candidate folder `1ZYI2jzrv7jN6OClu93mXFvIqSvHsbVnO` created; **files not verified uploaded to Drive**. Local preview SHA-256 `6245589cecb2298c467fa931341904ee8927a1939b5b791065dd7b6aeadeff43`; source ZIP SHA-256 `d7acc3b1e37f4442cb8587a7eee954edb7f5df6c27f797a012ff319881a`. Exact licensed Times New Roman production remains unavailable in this environment; local preview uses Tinos and approximately reconstructed shared style rather than a byte-identical fetched GitHub style. The GitHub source branch inherits the canonical shared v2.6.4 blob. No CURRENT Drive ID overwritten or re-pointed. The 144-rule university, final whole-page zoom, full parent result parity and academic signature checks remain open.

# Saugat Paneru — LATEX_SEQ032 source-edit QA and reviewer checklist
Date: 2026-11-01 NPT
Status: SOURCE-EDITED / PDF BUILD NOT PERFORMED / NOT CURRENT
Authority: RSH-002; parent LATEX_SEQ031 R2 user-designated CURRENT
Git branch: thesis/saugat-paneru/latex/seq032-figure-grid-review

## PRE preservation and restoration

- [x] Located SEQ031 R2 live PDF and full source ZIP; current pointer unchanged.
- [x] Created dedicated PRE folder [SEQ031 R2 archive](https://drive.google.com/drive/folders/1_BGwgjyAFJHK0GKtYxdKJTguz5pjlS0V).
- [x] Provider-readback of three enumerated PRE file copies: PDF 22,570,798 bytes (ID 1G651gWwgzSnZNJbdxr3YK-S142MtqqoV); ZIP 58,877,970 bytes (ID 1AdltwXf6cim3SjNvaoO0rpf1zNoCrTy2); pointer snapshot 5,424 bytes (ID 1MOBED8KZtRIl6Z92lK2d8rpVWUtyuQOc). Bytes match original metadata, independent hashes of copied files not freshly computed.
- [x] Kept previous live IDs: PDF 1FfNQpm8kslr5OcV0JxD76T4Ho6wMSMJm; ZIP 1putkQYpDff50kxycZJ33iPq98lb8I5mh; CURRENT_CHECKPOINT 1vXh7XUbkZcqzI1q8GFxZ1EcFHUKZhKQN.
- [ ] Final source+PDF rebuild, validation, POST copy and in-place CURRENT re-point **not done**. Do not promote based only on Git source changes.

## User 2026-11-01 numbered requests

| # | Request | Source status | Required visual/semantic QA |
|---|---|---|---|
| 1 | Eliminate mechanical figure-first paragraph openings across the paper | SOURCE EDITED for 17 exact paragraph starts in 10 content files; manual full-thesis language audit OPEN | Full PDF text scan for other variants and context/grammar |
| 2 | Figure 3.3 Regular only | SOURCE EDITED: singular regular plan figure | Compile and inspect numbered output |
| 3 | Figure 3.4 five irregular models L, L1, L2, T, U | SOURCE EDITED: grouped a–e in 2+2+1 horizontal layout | Check labels, all five visible and legible |
| 4 | Figure 3.5 Non-Parallel only | SOURCE EDITED | Verify numbering / image |
| 5 | Consistent figure-panel size, horizontal rather than stacked layout | SOURCE EDITED: fixed 0.48\textwidth and 0.18\textheight frame with aspect-ratio preservation; source model views 2-column 0.485\textwidth | Render page by page, inspect empty margins and readability |
| 6 | Small explanations after figures | SOURCE EDITED for three floor-plan groups and all eight source model views; conceptual GII explanation kept | Verify text appears after matching figures and doesn't float apart |
| 7 | Missing figures 3.9–3.15, rearrange model views | Eight original model asset paths remain referenced; grouped figures have **new automatically generated numbers**. Do not claim the old figure numbers persist | Full chapter Figure-map (SEQ031 -> SEQ032), check every referenced binary in full private ZIP and final PDF |
| 8 | Page 48 Table 4.4 normal template font | SOURCE EDITED Chapter 4 storey-shear summary: removed \small and \resizebox, set \normalsize; no numeric values changed | Confirm actual Table 4.4 identity and physical PDF page after reflow |
| 9 | Reviewer own DOCX items 9–22 still incomplete | VERIFIED prior record has mixed PARTIAL/BLOCKED/PRESERVED, not 14 completed items | See separate 22-point ledger below; final acceptance not claimed |
| 10 | New SEQ032, archive prior and preserve live IDs | PRE archive COMPLETE, Git source branch CREATED | Canonical sequence reservation PR, source/PDF archive POST, same-live-ID promotion pending |
| 11 | Correct margin and line spacing to governing standard | BASELINE SOURCE already declares left=3cm/right=2.5cm/top=2.5cm/bottom=2.5cm and body \onehalfspacing; no unsupported numerical replacement | PDF physical text bounds/line-leading per section and 144-rule audit |
| 12 | TOC CHAPTER N, newline TITLE, gap, then 1.1 etc. | Shared template v2.6.4 source prepared separately (RD-LTX-CHG-123); Saugat adapter switched to shared \PUPrintContents | Two-pass XeLaTeX, inspect all chapters including sections/page numbers |
| 13 | Shared template first, then Saugat | Separate template PR prepared; local Saugat shared-file inheritance retained | Template PR CI+merge, then rebase/check Saugat source PR |

## Previous 22 DOCX reviewer items — carry-forward audit

The controlling pre-SEQ032 ledger is researchers/saugat-paneru/latex/qa/SEQ031_22_COMMENT_SCOPE_AND_QA_20261101.md. These are its actual dispositions; SEQ032 does not silently upgrade all to COMPLETE.

| Reviewer item | Previously recorded | SEQ032 disposition |
|---|---|---|
| 1 Abstract | PARTIAL | UNCHANGED, supervisor wording verification pending |
| 2 TOC | COMPLETE | REOPENED for mandatory two-line/chapter spacing and PDF recompile |
| 3 LOF | PARTIAL | UNCHANGED; original embedded graphic fonts pending |
| 4 1.1 Background | ALREADY | PRESERVED |
| 5 Introduction graphic | COMPLETE | PRESERVED |
| 6 Fig 2.1 | COMPLETE | PRESERVED |
| 7 Literature diagrams | COMPLETE | PRESERVED |
| 8 Methodology flow | PARTIAL | UNCHANGED, screenshots not invented |
| 9 Models/GII | PARTIAL | SOURCE REWORKED: horizontal, grouped plan/model figures; visual QA pending |
| 10 Graph titles | PARTIAL | UNCHANGED; 14 historical plots unverified |
| 11 ULS drift | COMPLETE | PRESERVED |
| 12 Storey shear | PARTIAL | UNCHANGED source outputs; Table 4.4 font changed only |
| 13 Drift base | COMPLETE | PRESERVED |
| 14 Figure font uniformity | PARTIAL | SOURCE PANEL SIZING EDITED; embedded binary fonts remain unverified |
| 15 Torsion standard | BLOCKED_SOURCE | BLOCKED: raw rotation/case coordinates not available |
| 16 Capacity legend lower right | BLOCKED_SOURCE | BLOCKED: editable curve coordinates absent |
| 17 Enlarged detailed evidence | COMPLETE | PRESERVED |
| 18 Symbol patterns | COMPLETE | PRESERVED |
| 19 Discussion/conclusion | PARTIAL | UNCHANGED scientific wording; reviewer signoff needed |
| 20 Raw values | PARTIAL | UNCHANGED numeric source; ETABS replay pending |
| 21 Table narrative | COMPLETE | PRESERVED |
| 22 Side-by-side figures | PRESERVED | New paired model views only, remaining pairing requires visual legibility |

## Build/release validation gate

- [ ] Dedicated template PR merged and shared reference pinned to its merged blob SHA.
- [ ] Source-level GitHub CI, scope/ownership, no duplicate template.
- [ ] Independently restore all private figure PDFs/PNGs and original scientific assets from exact SEQ031 R2 source ZIP (do not publish binaries on public GitHub).
- [ ] Compile complete SEQ032 source using licensed Times New Roman, XeLaTeX/Biber, repeat passes for TOC/LOF/LOT.
- [ ] Check no missing paths, undefined refs, overfull, float-too-large, mis-sized pictures or fonts.
- [ ] Compare source numeric/data hashes to parent, check all 144 formatting rules and page 48 table in the newly paginated document.
- [ ] Audit 3.3/3.4/3.5, former 3.9–3.15, TOC each chapter visually.
- [ ] Save SEQ032 PDF+editable ZIP and figures intact into governed Drive candidate.
- [ ] PRE/POST checkpoint, full hashes, new version/sequence register, readback.
- [ ] Promote SEQ032 as user-designated CURRENT only after correct PDF/source outputs exist; academic signoff remains a separate factual status.

## Source references
- Parent user CURRENT checkpoint: https://drive.google.com/file/d/1vXh7XUbkZcqzI1q8GFxZ1EcFHUKZhKQN/view
- Parent complete source: https://drive.google.com/file/d/1putkQYpDff50kxycZJ33iPq98lb8I5mh/view
- Parent PDF: https://drive.google.com/file/d/1FfNQpm8kslr5OcV0JxD76T4Ho6wMSMJm/view
- Global format policy: controls/latex/template/pumlsc-shared.sty and controls/latex/audits/PU144_RSH002_CP114_M2_FROZEN_LIVE_20261020.md
- Scientific provenance issue #35 and formatting issue #34 remain open.
