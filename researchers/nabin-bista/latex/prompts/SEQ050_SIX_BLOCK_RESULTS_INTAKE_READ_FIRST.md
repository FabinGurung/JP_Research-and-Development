# Nabin Bista — exact governed LaTeX intake-to-manuscript prompt (candidate LATEX_SEQ050)

**Use in Nabin Bista's owning LaTeX chat only after researcher evidence is admitted.** This is executable task guidance, not scientific authorization to rewrite the current PDF.

PROJECT: RSH-003 Nabin Bista — *Seismic Fragility and Soil–Structure Interaction Based Performance Assessment of Mid-size General Hospital Buildings in Nepal*.

BOUNDARY: GIT-FIRST / A7 MEMORY WALL / SCIENTIFIC FAIL-CLOSED / NEVER DELETE / NO CROSS-RESEARCHER SCIENTIFIC CONTENT / SINGLE CURRENT GOOGLE DRIVE PDF ID / NO FALSE COMPLETION.

## 0. Authoritative read order and exact source resolution

1. Read `docs/GIT_DRIVE_AUTHORITY_READ_FIRST.md`, `controls/git-drive-authority.json`, `controls/latex/tower.json`, `registry/latex-build-profiles.json`, and the latest `researchers/nabin-bista/latex/source-and-drive-manifest.json` on `main`. Read A7 Memory Wall platform responsibilities and storage-only architecture. Code/version history = Git; original evidence and binaries = Google Drive; Actions = actual QA; Pages = public-safe directory.
2. In Nabin Bista's **existing fixed-ID Discussion Google Doc**, open **DISCUSSION CHAPTER 12 — Six-block Result Plots and Hospital Plan (29 October 2026)**; use the same document's owning private source-intake audit `NABIN_BISTA__20261029__RESULT_PLOTS_PLAN__SOURCE_INTAKE_MANIFEST_AUDIT_v1.0`. The audit includes exact new Google Drive source IDs, original names, SHA-256, the 14 label conflicts, and PRE/POST Discussion Doc snapshot links. DO NOT place these private IDs in this public Git repository or on Pages.
3. Provider-read the two uploaded originals from the **dated folder under 01_ORIGINAL_SOURCES**, and recompute SHA-256. Required archive hash: `c32844ec525745fc03dace9bee87515b793761476c4f2d54cc74f1f865d729e2`, bytes 29,784,990. Required plan PDF hash: `0a6b050f50dc05e895be0866216d29ac6aaa51aee2d92db6b6eff7038f0c1d5f`, bytes 495,095. Abort on mismatch.
4. Recheck Git `main` HEAD as PRE and latest permanent CURRENT PDF metadata/readback before writing. As of intake, the unchanged prior release is **LATEX_SEQ049**, 69 pages, with the usual permanent CURRENT Drive ID documented in the researcher manifest. **LATEX_SEQ050 is a conditional candidate**, NOT issued while the new data remain unadmitted.

## 1. Intake analysis — derive provenance, NOT unsupported thesis prose

- Preserve all 74 non-directory archive files and source identities: 67 XLSX workbooks across BLOCK 1–6 (11/11/11/11/11/12), six 3D PNGs and one earthquake-list TXT. There are 228 workbook tabs and 36 embedded charts. Avoid automatically treating any chart as independently validated.
- Enumerate each workbook/worksheet, source row, formula, unit, model name, block label, case name, direction, value and output SHA in a *private evidence manifest*. Preserve an append-only Source→Extraction→Derivation→QA→Admission mapping. Reconcile all **14** observed file/sheet block-label mismatches in the audit before production use, including BLOCK 2 STORY SHEAR B3 and the extra BLOCK 6 file labelled block 4.
- Establish whether the six blocks in the 1-page AutoCAD hospital plan are separate structures, connected wings, or partitions of a single structural model; map architectural drawing grids/floor labels to each ETABS analytical source. The plan is not proof that any particular workbook corresponds to the previous G+5 prototype.
- The submitted earthquake list names 12 records and proposed PGA steps 0.1–0.5 g; independently verify waveform source, time/acceleration units, station and component. Treat “barpark” versus “Barpak” as unresolved, not automatically an earthquake provenance correction.
- Fragility workbook filenames explicitly say X DIRECTION, but **filename text does not establish response-axis identity**; verify ETABS response output channel and raw time-history directions first. Never retrofit the older thesis fragility result's direction using the new filename alone.

## 2. Quantities to calculate — by block × support condition, not by guessed pooled averages

For every verified block (1…6) and support model (FIXED, HARD, MEDIUM, SOFT), with exact workbook/cell citation:

A. **Modal:** first-mode period `T1`, modal frequency, participation modes `UX/UY`, cumulative `SumUX/SumUY`, first mode satisfying ≥90% both axes; report status if the criterion is not met. B1 sample first-mode periods (s) = 0.856/0.861/0.878/0.929 (Fixed/Hard/Medium/Soft), **not** the old thesis 0.984/1.001/1.049/1.147 sequence. Resolve identity before replacement.

B. **Response spectra:** roof and inter-storey displacement for **exact same RSx/RSy, ULS/SLS load cases**; maximum ISDR by storey and direction (ratios vs percentages), shape of vertical profiles, base and storey shear. Handle sign conventions and units; preserve distinct load cases.

C. **Foundation:** max absolute `Uz` settlement under matching combinations, support-joint displacement/reaction, total vertical reaction equilibrium, location and footing identity. Do not compare 0-fixed settlement using a percentage denominator of zero.

D. **Forces:** beam shear V2/moment M3, column axial force/moment M3 with member IDs, location, sign, controlling case and actual envelope; avoid treating a workbook-wide extreme as member capacity.

E. **SSI sensitivity:** for every comparable numeric quantity and verified block, derive `100*(R_support - R_fixed)/R_fixed` from the exact common quantity, same units/case/direction; separately report absolute changes when `R_fixed=0`. State if the trend is non-monotonic and do not force “soft worst” without source.

F. **Fragility/IDA:** reconstruct each of 12 records × five PGA steps when source rows exist, by block/support and verified response direction. Confirm raw `%ISDR` formula, 0.5/1.0/2.0/2.5% boundaries of the current Table 3.5 and the older 1.5% DC modelling threshold; reconcile DS/DC label discrepancy. Recompute mean threshold PGA, uncertainty/dispersion, lognormal exceedance `P(DS>=ds|PGA)`, 0.1–0.5g measured domain, extrapolation, and all plotted curves from actual cells. If source only supplies synthesized outputs, call these *reproductions of submitted workbook calculations*, not independently observed event damage.

G. **Block-level synthesis:** build an evidence-qualified table/figure inventory; an aggregate six-block hospital conclusion only if architecture, mass/system coupling and aggregation rule are verified. Never silently average disconnected block analyses.

## 3. Scope reconciliation and exact manuscript change map

- Compare new 6-block outputs with the existing **single-prototype** LATEX_SEQ049 tables/figures/text. The initial modal values differ even at Block 1; therefore **do not replace Chapter 3/4 or the Abstract automatically**.
- For each proposed edit, register: old section/table/figure, new proposed academic caption, sources, formula/method, model identity, scientific interpretation, uncertainty, and `ADMITTED / PARTIAL / HOLD / REJECTED`.
- Potential sections affected only after approval: §3.3 prototype/hospital model and plan; §3.5 foundation SSI; §3.6 linear quantities; §3.9–3.10 records/fragility; §4.2–4.7 block response; §4.10–4.11 nonlinear/fragility; Chapter 5 conclusions. Preserve unrelated manuscript paragraphs, citation IDs and original manuscript voice.
- Protect established September 2026 title pages, examiner/coordinator names, corrected Table 3.5 performance bands, abstract sentence removal, Figure 4.18 natural caption and prior source limitations unless exact new evidence and user direction authorize changes.
- No manufactured seismic outputs or scientific references. Do not infer unprovided ETABS model files, station IDs, foundation ties, directions, beam member capacities or numerical rates.

## 4. Version-control and release sequence (only after scientific admission)

1. Re-read Git `main` HEAD and current fixed-ID PDF. Create a fresh **Nabin-specific** branch on latest `main`; preserve every earlier branch, commit, historic source and Drive link. Keep `main_SEQ049_original.tex` intact. Scientific source/code into `researchers/nabin-bista/latex/`; no private spreadsheets/images/fonts/PDFs in public Git.
2. Record Git PRE SHA, exact incoming source provenance and human-readable Discussion DOCREV01 POST. Admit validated analysis via bounded Discussion→LaTeX handoff, **not** by scraping raw discussion prose.
3. Prepare LATEX_SEQ050 only if SEQ049 still CURRENT and authorized. If using the single canonical shared `pumlsc-shared.sty`, explicitly port the legacy main entrypoint and complete independent formatting parity; the old source uses BibTeX and `main.bbl`, whereas the universal default uses Biber. Preserve bibliography and the two previously recovered source figures; fail if References disappear or citations unresolved.
4. Build a complete candidate PDF, render and inspect **every physical page** and all tables, graphics, formulas, captions, bibliography, chapter TOC/LoF/LoT, front matter and pagination. Compare changes to the 69-page SEQ049 baseline, explaining any page-number shift; do not mandate a fixed 69 pages after valid new content.
5. Archive immutable candidate source ZIP and compiled PDF in Nabin's existing dedicated Drive archive; verify provider IDs, bytes, hashes and page count. **Only on final verified promotion**, replace bytes of the SAME permanent CURRENT PDF ID while preserving previous CURRENT in archival storage. Never fabricate upload/QA completion.
6. Create a **new version-specific audit Google Doc** (not rename the old SEQ46 audit), with original-file inventory, cell/method provenance, risk flags, PRE/POST Git SHAs, exact change map, discrepancy resolution, all-page QA, verified Drive file identities and scientific HOLDs. Preserve the existing fixed-ID Discussion Doc; significant new scientific discussion must get its own PRE and POST checkpoint copies, with exact native Google Docs revisions. Do not advance routine A9 Local/Main sequence counters solely for Git source history.
7. Pass GitHub Actions source/LaTeX checks, perform independent compilation QA, then PR/merge and provider-read. GitHub Pages may show **public-safe status and approved links only**, with deployment checked separately. A passing Actions job never implies university/supervisor approval.

## 5. Stop conditions and required report

Stop before manuscript mutation if the six-block geometry/scope remains ambiguous, the 14 mismatches are not reconciled, source units or ground-motion records are unverified, bibliography is missing, or 69-page baseline QA cannot be compared.

Deliver to researcher before writing: (1) model/block mapping matrix; (2) 67-workbook/228-tab source catalog with SHA/cell provenance; (3) 14-flag QA disposition; (4) derivation scripts and reproducibility tests; (5) candidate figures/tables with source references; (6) bounded `ADMITTED/HOLD` manuscript edit map. No claimed LATEX_SEQ050 release until the governed PDF + audit Doc chain actually exists.
