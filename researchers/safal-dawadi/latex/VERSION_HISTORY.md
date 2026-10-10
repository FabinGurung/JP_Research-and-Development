# Safal Dawadi — Git-controlled LaTeX version history

**Latest working manuscript:** [v1.12](https://github.com/FabinGurung/JP_Research-and-Development/tree/safal/v1.12-building-only-cover-spacing-20261010/researchers/safal-dawadi/latex/manuscript)

| Source version | Git ref | Purpose | Status |
|---|---|---|---|
| v1.9-fmt-r1 | [main (read-only scientific baseline)](https://github.com/FabinGurung/JP_Research-and-Development/tree/main/researchers/safal-dawadi/latex/manuscript) | 40-page technical review | Preserved; original source approval remains HOLD |
| v1.10 | [safal/v1.10-photo-snapshot-20261010](https://github.com/FabinGurung/JP_Research-and-Development/tree/safal/v1.10-photo-snapshot-20261010/researchers/safal-dawadi/latex/manuscript) | Initial 25-photo source integration | Frozen fallback/snapshot; not publication certified |
| v1.12 | [safal/v1.12-building-only-cover-spacing-20261010](https://github.com/FabinGurung/JP_Research-and-Development/tree/safal/v1.12-building-only-cover-spacing-20261010/researchers/safal-dawadi/latex/manuscript) | Building-only research scope; all road matter removed; adjusted cover logo spacing | LATEST REVIEW, source build pending |
| v1.11 | [safal/v1.11-authorial-revision-20261010](https://github.com/FabinGurung/JP_Research-and-Development/tree/safal/v1.11-authorial-revision-20261010/researchers/safal-dawadi/latex/manuscript) | Correct author voice, human figure captions, remove machine codes, preserve limited evidence conclusions | Latest **source-review** candidate; production PDF and author approval pending |

The former photo review PR #6 remains a historic predecessor; v1.11 is [draft PR #7](https://github.com/FabinGurung/JP_Research-and-Development/pull/7).

## Single template — actual invocation
Do not create a researcher-specific duplicate base formatting package. `main.tex` uses:

```latex
\usepackage{pumlsc-shared}
```

The only canonical shared style is [pumlsc-shared.sty](https://github.com/FabinGurung/JP_Research-and-Development/blob/main/controls/latex/template/pumlsc-shared.sty). Make that directory available on `TEXINPUTS`, then compile from `manuscript` with **XeLaTeX → Biber → XeLaTeX → XeLaTeX**. The private licensed Times New Roman installation is mandatory for an official format review. Optional `\def\PUPreviewTinosFont{}` is a non-certified preview fallback only. Use the approved source and compatible reader-facing project-specific settings; do not regress to `pu_fst_final_report.sty` for a released PDF.

## Confidential photographic assets
The source references 25 `private_photos/SAFAL-PHOTO-*.jpg` files, which **must be supplied for an authorized local build**. Images remain in controlled Google Drive, not in the public Git repository. The code is deliberately compilable with visible *missing-photo* placeholders so a source check cannot pretend the image assets were present. A PDF with missing-photo placeholders must never be treated as the finished paper. Preserve original photo IDs only in source image paths, not printed captions.

## Student authorship and semantic QA
- The present authorial revision is a proposed draft for Safal's first-person scientific review, not a declaration that AI did no writing.
- Students must review the prose to confirm that each first-person claim describes a real observation/activity. Never invent costs, dates, tests, interviews or conclusions.
- The universal [authorial voice policy](../../../controls/latex/authorial-voice-policy.json) is proposed; it must be centrally approved before it becomes binding for other researchers. The typographic template cannot automate individual authorship.
- Source snapshots are versioned **before** producing PDF outputs. Preserve the Git SHAs, build manifest, private font/image dependencies, full-page PDF QA and A9 closeout.
- The public R&D website baseline is unaffected. The manuscript's private final-submission status is unchanged.

## Release gate
1. Safal reviews and approves every new first-person assertion and photograph caption.
2. Real site/photo/source relationships are documented as applicable; road-PCC examples stay comparative.
3. PDF compiled from exact v1.11 Git source ref, with 25 photos and private licensed Times New Roman.
4. Validate full rendered document and bibliography; record source SHA, PDF SHA and font list.
5. Governed A9 Local registration and Main ACK only when separately authorized.
