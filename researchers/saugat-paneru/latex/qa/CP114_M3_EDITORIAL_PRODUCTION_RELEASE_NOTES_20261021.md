# Saugat Paneru — M3 approved editorial-production milestone

**Tag:** `saugat-cp114-m3.0.0-editorial-production-20261021`  
**Current production:** `CP114-GIT-v2.4-DISC-V024-S02-20261021`  
**Scientific authority:** CP114 unchanged (this is **not** a new scientific CP115).  
**LaTeX format:** shared PU v2.4, exact Times New Roman build.  
**Authorization:** User directly approved the editorial change and promotion to CURRENT on 2026-10-21.

## Actual finished product

- **[CURRENT compiled 115-page A4 thesis PDF](https://drive.google.com/file/d/1NRLCgy7F8vIMzGs03zadiVC8SsuhEh5J/view)** — 55,178,306 bytes, SHA-256 `b08e3ebb1ea1849d25cf07e69bf77492099a99acb3cb24889c44db46a449c342`.
- **[CURRENT complete source-and-research-asset ZIP](https://drive.google.com/file/d/1Ts1BniRbLb_Ft9fiBME2LsKsIfr0CCzR/view)** — 58,642,661 bytes, SHA-256 `9fc5c47ecdde9c788c9678d9fd31b41aed41b6e6b15dbf555f514d12297504bd`.
- [Production folder](https://drive.google.com/drive/folders/19l-Cm48gA-JnaGd4MFl63EOq-MelKpcD) and **same-ID** [Drive CURRENT_CHECKPOINT](https://drive.google.com/file/d/1vXh7XUbkZcqzI1q8GFxZ1EcFHUKZhKQN/view), provider readback verified. Both binaries copied and independently downloaded with exact SHA-256 matches.

## Precisely what changed since accepted CP114/v2.4

1. **Abstract:** incorporated bounded supervisor S02 editorial improvements while retaining the governing cases and all admitted CP114 findings.
2. **Chapter 5 Conclusions:** changed artificial Objective 1–6 numbered prose into connected engineering paragraphs without inventing results; Recommendations preserved.
3. **Table 4.24:** updated the six objective/result/conclusion cross-references to the thematic paragraphs rather than obsolete numbered conclusions.

Source [PR #37](https://github.com/FabinGurung/JP_Research-and-Development/pull/37) merged at `bb70dc2e2bed78bf25a8dda6530507577731faad`, then [production register PR #38](https://github.com/FabinGurung/JP_Research-and-Development/pull/38) merged at `3190958cfb5148751bbe68ccf4c565a35f56f024`. Both PRs passed **all three repository CI checks**.

**Scientific content was preserved:** 143/143 original CP114 research assets, no ETABS model rerun, zero new scientific claims. Full XeLaTeX/Biber with exact GitHub shared template + Saugat adapter compiled 115 A4 pages; 111/115 pages have identical normalized PDF text, while physical pages 10, 89, 90 and 91 reflect approved edits; 81/81 original embedded image placements, no overfull boxes, 252 inherited underfull hboxes (recorded).

[35-item supervisor discussion audit](https://github.com/FabinGurung/JP_Research-and-Development/blob/main/researchers/saugat-paneru/latex/qa/DISC_V024_S02_35_ITEM_NEXT_LATEX_ADMISSION_LEDGER_20261021.json): **19 already present, 4 integrated here, 6 source-gated, 4 deferred, 2 visual-review pending**. No attempt to falsely mark them all solved.

## Release debt boundary

**Zero unresolved release-blocking work for the user-approved three-file editorial update.** This is a scoped editorial-production release only.

**Open debt is explicitly NOT certified/completed:**
- [Issue #34 — university format 144-rule independent certification, figure-label legibility, inherited format exceptions](https://github.com/FabinGurung/JP_Research-and-Development/issues/34).
- [Issue #35 — underlying scientific/ETABS provenance, EQx/EQy, pushover metadata, unmatched height analysis](https://github.com/FabinGurung/JP_Research-and-Development/issues/35).
- Remaining 12 source-gated/deferred/visual supervisor items require separate evidence or editorial review. 144/144 code conformance and a signed university certificate have NOT been established.

## Permanent immutable rollback

- [Previous CP114 v2.4 formatted PDF](https://drive.google.com/file/d/1tuXDpv1eP9bPqVbLfqimmRMQTQo8Eqvg/view), SHA-256 `5bbe2bcf006f16f823e796ca9c6722c122de69c27cec7955803d98b07b6d3428`.
- [Previous CP114 v2.4 complete source](https://drive.google.com/file/d/1eMgFKcjYin6SIO4-SUC1d70c1qADttOi/view), SHA-256 `425f125ec3f19d48215cfbf559b1180bea2154b09940b2d8022e7b4183f25ac8`.
- [PRE-CURRENT snapshot](https://drive.google.com/file/d/1fCKIowI1_bxKohTmXPdwy9r-NCfN2_dI/view), exact provider readback.
- [Prior M2 frozen-source/QA GitHub milestone](https://github.com/FabinGurung/JP_Research-and-Development/releases/tag/saugat-cp114-m2.0.0-source-qa-20261020), archived CP114 science and every original research asset preserved.

**This M3 version controls an approved, finished editorial thesis PDF, not a blanket scientific or university certification.** Full PDF, workbooks, research figures and licensed font files remain in governed private Drive custody and are not attached as public GitHub assets. 
