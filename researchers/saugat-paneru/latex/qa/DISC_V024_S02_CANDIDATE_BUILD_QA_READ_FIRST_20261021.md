# Saugat Paneru — Discussion V024 / S02 Minimal Manuscript Candidate

**Disposition:** QA candidate only; NOT merged, NOT production CURRENT, NOT CP115 or a release. Parent scientific content: CP114, production v2.4; M2 remains immutable.

## Current authority inspected live (2026-10-21)

- GitHub main PRE: `ac3384d36f155433e98a4ce47d1ee462c1bbcb7c`.
- Central shared PU source: `controls/latex/template/pumlsc-shared.sty`, **v2.4**, exact Git blob `6fb77b6f09773e29bd1159a4dc4ec2d7f773aa06`.
- Saugat adapter: `researchers/saugat-paneru/latex/extensions/saugat_project_adapter.sty`, exact Git blob `242418f5f4f14cf325f77833596717981322e7d3`. Both verified byte-for-byte inside local test build; no global style change.
- Active scientific/production [CURRENT](https://drive.google.com/file/d/1vXh7XUbkZcqzI1q8GFxZ1EcFHUKZhKQN/view) and [115-page PDF](https://drive.google.com/file/d/1tuXDpv1eP9bPqVbLfqimmRMQTQo8Eqvg/view) remain immutable.
- Verified [Discussion V024 35-item S02 matrix](https://docs.google.com/document/d/1lF5WKoido1Tzgk6D9ZFLbkVjV3TCwZinrNnLfVF7bA0/edit), original [S02 source](https://docs.google.com/document/d/1s1LlfTSw2j_gF8cNYBuBhuNvTGz7u7B-w3yJa6xqxA4/edit), and [M2 release](https://github.com/FabinGurung/JP_Research-and-Development/releases/tag/saugat-cp114-m2.0.0-source-qa-20261020).

## Three source edits only

1. `frontmatter/abstract.tex`: replace the existing abstract with a conservative S02-informed revision, retaining exact CP114 admitted model/case/direction/limit boundaries, introducing only original CP114-reported 2012 failures and Non-Parallel CM–CR context. No new scientific dataset or invented result.
2. `chapters/chapter5_conclusion.tex`: replace numbered Objective 1–6 submission prose with thematic connected engineering paragraphs; retain every six-objective finding and original numeric value, plus modal finding and 2012 reference evidence. **Recommendations section unchanged word-for-word**.
3. `cp112_additions/ch4_gii_summary_traceability.tex`: update 6 conclusion link labels so objective/result crosswalk no longer cites nonexistent numbered conclusions.

[35-row admission ledger](DISC_V024_S02_35_ITEM_NEXT_LATEX_ADMISSION_LEDGER_20261021.json): **19 already present; 4 candidate edits implemented; 6 source-gated; 4 deferred; 2 visual review.** Not all 35 newly implemented.

## Build & PDF verification — successful

- Local complete CP114 original source assets restored from frozen M2 ZIP and verified **143/143 SHA-256 unchanged** (77 PNG, 58 PDF, 7 XLSX, 1 JPG).
- Exact current shared style and exact project adapter transplanted from Git source, both content SHA/blobs verified.
- XeLaTeX (4 passes) + Biber with private exact **Times New Roman**, followed by xdvipdfmx; no proprietary fonts distributed.
- Candidate **115 A4 pages**, unchanged per-page normalized text on **111/115**. Only physical PDF pages **10** (Abstract), **89** (table traceability), **90–91** (conclusions) differ.
- 81 embedded raster image placements before, 81 after; zero out-of-physical-page text spans, zero overfull boxes; 252 inherited underfull hbox warnings documented, not silently called fixed. No undefined citations or fatal TeX errors reported.
- Original figure labels under 10pt (issue #34) and scientific-source gaps (issue #35) remain explicitly deferred.
- Changed pages 10, 89–91 rendered to PNG and visually inspected; unchanged table/figure/reference content and 115-page overall pagination validated.

## Drive deliverables — provider download and SHA readback MATCH

- [Candidate compiled PDF](https://drive.google.com/file/d/1ZMBpPWGV4Kv6MzYHuM0XOgJr1u-sN_OG/view) — 55,178,306 bytes; SHA256 `b08e3ebb1ea1849d25cf07e69bf77492099a99acb3cb24889c44db46a449c342`.
- [Complete candidate 221-file ZIP](https://drive.google.com/file/d/10-yUstfX6lrsMEJLvsBRDVj_tlDhtudE/view) — 58,642,661 bytes; SHA256 `9fc5c47ecdde9c788c9678d9fd31b41aed41b6e6b15dbf555f514d12297504bd`.
- [Dedicated Drive QA folder](https://drive.google.com/drive/folders/19IlMp97jbORBYfp4cX-JSYchA4z2V6LF). ZIP contains candidate QA report and source diff; no font binary included.

## Non-promotion rule

Do NOT merge, tag, release or replace CURRENT as a side effect of Discussion intake. Await manuscript editorial review and GitHub CI before seeking explicit production promotion. CP114 + M2 are the fixed rollback. This record is source-and-render QA evidence, not university 144/144 certification.
