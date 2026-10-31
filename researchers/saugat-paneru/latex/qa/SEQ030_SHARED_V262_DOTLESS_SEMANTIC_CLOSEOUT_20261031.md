# Saugat LATEX_SEQ030 — shared v2.6.2 navigation + semantic review (source QA receipt)
**Owner:** RSH-002 / Saugat Paneru. **Scientific CP:** CP114 unchanged. **Status:** QA_CANDIDATE; no current production promotion, no supervisor approval claim.

## Why this version exists
- SEQ029 was pinned to shared template 2.6.1, and its 120-page PDF predated the global all-list dotless change.
- The single shared `pumlsc-shared.sty` was already promoted by an independent global PR to v2.6.2 on main (Git blob `491538d53f83023af0b485dc0251728688ec4e2a`), tracked as `RD-LTX-CHG-120`. **No new template fork** or second master was created.
- `1.1 Background` in Saugat is correctly defined as `\chapter{Introduction}` followed by `\section{Background}`; the shared `.sty` already formats section numbers universally. Its specific scholarly wording must not be copied to other researchers.
- Earlier M4.2 11-file manuscript prose review PR #66 was unmerged; SEQ029 accidentally retained the old status table and administrative section. SEQ030 integrates those changes with the newer SEQ029 supervisor methodology work, preserving source-grounded values. The overlapping Ch1, Ch3 and GII edits were three-way merged against exact original M4.1 base and compared to locally built file Git blobs. No empirical outputs re-run or invented.

## Actual local PDF and source proof
- Exact shared v2.6.2 blob SHA `491538d53f83023af0b485dc0251728688ec4e2a`; authorial voice shared semantic policy v1.3.0.
- Four XeLaTeX source passes plus Biber, no overfull box build gate. Ghostscript optimized PDF has **120 A4 nonblank pages** and embedded TimesNewRomanPSMT, TimesNewRomanPS-BoldMT, TimesNewRomanPS-ItalicMT. SHA256 `2a35732e7d1899d3857458a43465d1e3b6374ea83ffa6fa0b2f9b6c4601e576d`, 22,382,335 bytes. No proprietary font in public GitHub or source ZIP.
- Rendered nav pages (TOC p.11, LOT p.13, LOF p.15, equation list p.18, appendix list p.19): **zero dotted-leader runs**, page numbers visible at right, `1.1 Background` in TOC.
- Old `Hinge evidence available for the seven-model comparison` administrative Table 4.21 text and `Alignment of Research Questions, Results and Conclusions` editorial mapping removed. New `Interpretation of the Comparative Findings` appears, citing specific existing results; auto table numbering now makes a *different substantive GII Table 4.21*. This is correct and not a resurrected status table.
- Complete 233-entry source ZIP SHA256 `104dd62e4535bd5f33a73248bb1a2b2cd6eda4c1bba434b7dcebbce2d44842a4`, 58,668,313 bytes, ZIP CRC pass. **143/143 original binary research assets** byte-identical to SEQ029; no embedded fonts or build cache.
- Original accepted CP114 M4 PDF and permanent live Google Doc untouched. Editorial changes do not imply ETABS input correctness, code approval or new scientific admission.

## Explicit incomplete control-tower gates
- The source-based 144-entry PU rule audit on main (`controls/latex/pu-format-parity-audit.json`) has 144 mapped requirements but does **not** certify all implemented/verified. Historical audit counts: 7 source-declared, 47 partial/policy, 90 missing/unverified and 0 fully production verified as of that audit. This source-format ledger must be independently re-audited against actual compiled SEQ030; 120p technical QA is not 144/144 approval.
- Native Google Doc/Word equivalence remains unproven; previous SEQ029 candidate exported 109p versus 120p LaTeX. **No claim of parity for SEQ030**, and the permanent LIVE Google Doc remains unchanged.
- Researcher/supervisor signoff and full university submission acceptability remain pending. Exact ETABS member-level hinge inventory/other prior scientific data limitations must not be invented to close a checklist.
- Drive candidate folder was created `1fK6NHNAohnv28jCoLGThADitb4ZPAAjy`. Upload through Files failed with `container_session_expired` and **must not be represented as uploaded** until actual provider ID/readback exists; local artifacts and their hashes remain available.
- PR source checks, protected-main merge, Drive proof and current release promotion are separately verifiable events. No shared `.sty` was edited in this researcher PR. No historical Git refs or approved M4 artifacts deleted/repointed.

**Restoration:** Previous seq029 manifest SHA, original M4 production pointers and current LIVE Docs ID preserved. Any future accepted revision must take enumerated PRE/POST snapshots, validate provider file bytes and update the same IDs only after parity and approval.
