# RSH-002 / Saugat Paneru — M4.1 42-item supervisor QA (2026-10-30)

**Scientific baseline: CP114, unchanged.** **Shared template: PU v2.4, untouched.** **Status: source-backed QA candidate; not merged/current/released.** Git PRE `d6936bb783218faf22bcf15f3dd36a231611407e`.

### Verified candidate artifacts
- [115-page A4 PDF candidate](https://drive.google.com/file/d/1D86hsXE986DnYwuuSnxIChOG6SwP9Ijn/view) — 22,326,623 bytes; SHA256 `59954cbb428f3e655da8d36238bc967fe4a5e3f7eb20dd60e55dff5ab3d87f91`.
- [Complete source ZIP including QA and 143 original scientific assets](https://drive.google.com/file/d/1gPl9iC1PzJGWVC8CywPl1YwNfUR4wiWC/view) — 58,666,533 bytes; SHA256 `8561e50e971146f36c021282084aadd6a29fda41abe4e72779ae3bb93b3c0172`.
- [Human-readable 42-item report](https://drive.google.com/file/d/1BEa0AbSHH3MJwdL3UaNdDjJmjyvumM9k/view) and [machine-readable QA ledger](https://drive.google.com/file/d/1wGpaYgGVlwV3sQYr-lOGMJY6Zj1ycspL/view).
- Independent Drive raw-file downloads SHA256 matched local PDF, ZIP and report. No binary fonts packaged.

### Three source files changed; no research figures/datasets mutated
1. `manuscript/frontmatter/keywords.tex` — include the full study-defined `Geometric Irregularity Index` in Keywords as in supervisor S03; compact axes still use GII with an established first definition.
2. `manuscript/chapters/chapter1_introduction.tex` — remove duplicate CM--CR eccentricity phrasing.
3. `manuscript/cp112_additions/ch4_gii_summary_traceability.tex` — visual check confirmed Figure 4.34 and later Figure 4.37 plot the identical seven-point GII/PP-shear relationship with alternate design. Remove later redundant **manuscript placement only**, retain the graph files and original scientific values. Repair reference to original figure; describe seven-model traceability without obsolete “five” count. Keep the objective/result/conclusion heading, explanation and Table 4.24 on one page.

### Build + print QA
- Four XeLaTeX passes plus Biber and two final XeLaTeX refresh passes completed. Full 115-page XDV converted with xdvipdfmx and compressed with Ghostscript `/prepress` to valid, selectable-text, unencrypted 115-page A4 PDF.
- No LaTeX fatal errors or overfull boxes in final XeLaTeX log. PDF preflight: opens normally, not scanned-only, no blank pages, no off-page text, no placeholder text. Original 143 CP114 scientific assets independently rehashed: **143/143 SHA256 exact match** (58 PDF, 77 PNG, 7 XLSX, 1 JPG).
- 107/115 normalized page text layers match the approved M4 current. Changed pages: **10, 14, 16, 17, 19, 87, 88, 89**; changes reflect Keywords, LOF/TOC, redundancy removal, Table 4.24 page flow. Ghostscript may re-encode image XObjects, so the output PDF's object count is **not** interpreted as a changed scientific source count. Original scientific figure files were never replaced.
- Current compiled PDF with unchanged label: [M4 CURRENT](https://drive.google.com/file/d/1QLnRQrXQm9Y_gqrCLzcEjkht6MlXIkjk/view). It remains the canonical production reference until separately authorized promotion.
- Earlier M2/M3 releases, original CP114 source and M4 rollback preserved.

### 35 S02 + seven S03 supervisor instructions
35 S02 were previously: 19 present, 4 completed in M3, six source-gated, four deferred, two awaiting visual QA. **Both visual-review items** are now tested against actual artwork; candidate removes redundant second base-shear plot. The 6 missing-science gates (material/model details, actual spectrum cases, pushover node/steps/hinge assignments, EQy shear) cannot be invented. C4-04 percent-case audit and other source-dependent requirements remain open.
Seven S03: abstract and conclusions already source-reconciled in M4; three-method introductory TikZ figure present; full GII keyword now included; co-supervisor `Er.` from user-supplied shared certificate but institution and professional title not independently confirmed; student's own-voice signoff is still a human action.

The original NBC 205 historical year **1994** was verified against the official Nepal Government code cover: https://giwmscdntwo.gov.np/media/app/public/54/posts/1679824458_45.pdf — S02's 1995 mention should not replace that primary authority. The new thesis candidate does **not** conclude universal RUD applicability, whole-building torsional compliance, a quantitative height effect, or member-level hinge results without evidence.

**Outstanding debt:** scientific [#35](https://github.com/FabinGurung/JP_Research-and-Development/issues/35), format/figure labels and 144-rule certificate [#34](https://github.com/FabinGurung/JP_Research-and-Development/issues/34), co-supervisor credentials/affiliation and researcher authorial review. This report is not a signed university-format or scientific certification.

**Version-control boundary:** one branch for M4.1; no global shared template edit, no Nabin researcher file, no Drive CURRENT mutation, no new CP115 or Git release tag. The release and production pointers require separately passing CI, explicit source approval and readback gates.
