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

## M4.2 editorial review (separate branch) — 2026-10-30

**This section is an audit addendum, not a revised M4.1 completion certificate.** On branch `saugat/m4-1-prose-and-audit-separation-review-20261030`, the student-facing source was edited to remove internal evidence-status prose and tables: former Table 4.21 seven-model hinge status matrix, the repeated “hinge evidence” prose and column in the final response summary, and the administrative objective/traceability table in former Section 4.7.3. Section 4.7.3 now discusses admitted results, including the seven-model force, drift, CM–CR and GII differences. Chapters 1–3 and 5 were also streamlined to state methods and conclusions rather than complain about missing inputs. The original figures, numeric values and scientific source remain unchanged.

All displaced source limitations and objective coverage are recorded in the **Google Doc audit**, stable ID `15IK5qfu4143tpVZpCXfFY-o2pQY5qkkyW9wzVH5n5To` (https://docs.google.com/document/d/15IK5qfu4143tpVZpCXfFY-o2pQY5qkkyW9wzVH5n5To/edit), in the existing 42-item QA, and applicable source manifests. Do not interpret the removal of an administrative status table as completion of any outstanding ETABS/model/hinge/matched-four-storey analysis.

**Full source build:** 114 A4 pages; XeLaTeX/Biber/xdvipdfmx and Ghostscript `/prepress`; PDF SHA256 `b1d2f286afb1f6c36f0e0dd0f1d50a5121f6a184a20e208ef6b6ca30f7473b7f` (22,257,188 bytes). The original 58 PDF scientific assets in the source manifest match 58/58 byte hashes; all original figures, charts and model records were retained. No blank pages or out-of-page text blocks; no failed source references detected in text preflight. The available build used **Tinos fallback**, not licensed exact Times New Roman; therefore it is a **preview, not university-font-certified production**. Source ZIP SHA256 `f80e0d4649e6b74326e0a7b00e05ac7bf97aaa615fcd8a51812eabd0f467611e` (58,665,222 bytes), ZIP integrity check pass.


### M4.2 final additional editorial cleanup and rebuilt preview (supersedes the preceding provisional file hashes)

Further source review removed the redundant "governing available case" column and the internal force-scale-anomaly status note from the EQx storey shear summary (all seven numerical EQx shear values kept). The four-storey failure image paragraph was rewritten as a normal scope-bounded description. The source was rebuilt from the modified LaTeX with two additional stabilized XeLaTeX passes, full xdvipdfmx conversion, and full PDF text preflight. Ghostscript second-pass compression was not completed and must **not** be claimed for this final file.

**Final current candidate downloads (external to Git):**
- 114-page A4 XeLaTeX Tinos preview PDF, 55,056,416 bytes, SHA256 `81cebc8f0fffbaa6d7f76f21012b183353832297aa09e4be39c8fa4f6fb6eb67`
- Complete edited LaTeX/source ZIP, 58,665,013 bytes, SHA256 `8e7427b961a5e021d166cb45fd4840b984379f1d45dc6c8ef6e0a550141d3d98`
- Compared all **143/143** original scientific binary assets to the original Drive M4.1 source archive (58 PDF, 77 PNG, 7 XLSX, 1 JPG): each exact SHA256 byte match.
- PDF: 114 A4 pages, nonempty selectable text throughout; absent-source whining/status phrases eliminated from chapter source, former Table 4.21 absent, former administrative Section 4.7.3 replaced by "Interpretation of the Comparative Findings".
- Exact Times New Roman still unavailable in this preview environment; **NOT production-certified**; M4 remains CURRENT.

**Version status:** unmerged review branch; not a new scientific CP, not a reserved `LATEX_SEQ029`, not a promotion of CURRENT, and no claim that 42/42 supervisor evidence gates have been fulfilled. Scientific approvals and exact-TNR production build remain distinct. Shared semantic-policy change is proposed in a **separate** governance branch, not mixed with the Saugat thesis branch.
