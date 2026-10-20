# CP114 source migration — binary completeness / Drive QA closeout (2026-10-20)

**Researcher:** RSH-002, Saugat Paneru  
**Classification:** source migration + format-only technical QA  
**Change:** RD-LTX-CHG-108  
**Scientific accepted CURRENT:** [CP114 PDF](https://drive.google.com/file/d/1aFVnwamHhp2Xpjmg10UfMPBwK031HMTh/view); [source archive](https://drive.google.com/file/d/1yL3G-EUGA32FDBhkdImXk9NManfW_vyA/view); these are untouched.

## Root cause and correction

The source ZIP initially delivered with the v2.4, 3×-logo build omitted **58** referenced CP114 PDF figures. A build from a clean extraction stopped at `figures/ch3/floor_plans/regular_floor_plan.pdf` rather than being reproducible. The old source QA ZIP must not be used as the final migration package.

The accepted CP114 source archive SHA256 `3af05ae5647de3311ac2941c387d3513fe76a5d29e8d6b6aaae152fb1a653bef` was verified. Its **143** binary research assets (58 PDF, 77 PNG, 7 XLSX, 1 JPG) were copied without alteration into the complete source ZIP and checked against individual hashes. All **32** protected subordinate scientific .tex/.bib modules remain byte-identical to CP114. The legacy duplicated `pu_fst_thesis.sty` is intentionally not included.

## Governed Drive QA binaries: uploaded and independently re-downloaded

| Artifact | Drive ID | Verified SHA256 | Size |
|---|---|---|---|
| Corrected exact-TNR 115-page v2.4 QA PDF | `10tMkCe8gh0oDXT5qV7c3txU-J9bGfl1v` | `5bbe2bcf006f16f823e796ca9c6722c122de69c27cec7955803d98b07b6d3428` | 55,177,712 B |
| Complete 213-file standalone source QA ZIP | `1dHZYKN8sD36m88RkVriTLRa_gAfhwjmA` | `425f125ec3f19d48215cfbf559b1180bea2154b09940b2d8022e7b4183f25ac8` | 58,591,934 B |

Parent folder [Git migration QA candidates](https://drive.google.com/drive/folders/1Nz2CRnrnYvRXEFHzs29mdvWWw3bPIgGi); [143-assets hashed source manifest](https://drive.google.com/file/d/1lEFyFY8MMG0P6NuZV7Ihk434zBqPLO5-/view); [latest Drive READ FIRST](https://drive.google.com/file/d/16atxKfC-Y4nbLpuVtUMliunN30Jl23pI/view). The original 116-page candidate is retained as historical evidence.

An extra identical PDF copy arose during transfer. It was independently re-downloaded, verified SHA256-identical to the canonical QA PDF, and **archived, not deleted**, at [noncanonical duplicate archive](https://drive.google.com/drive/folders/1Hwk4AuuMtSLtGX889oxid05b7pzNhZPu).

## Independent fresh-source rebuild

From a new extraction of the complete 213-file ZIP, with the legally held private Times New Roman fonts installed, `bash build.sh production` completed XeLaTeX/Biber/XeLaTeX stabilization and 115-page PDF generation. Rebuild PDF SHA256: `dba7b89a1c345e5dff9df09aa7bd463985c4bab70e4ea9d47bce71a10868c86e` (different container-generation binary, but exact extracted page text equals the uploaded PDF on **all 115 pages**, 81 embedded image occurrences in both, matching enlarged logo bounding box). No missing assets, no overfull warnings on final TeX pass. The converter logs nonfatal compatibility warnings when embedding version-1.7 figure PDFs into the PDF-1.5 default output.

## Git-source reconstruction contract

The public Git repository stores editable manuscript text, this `asset-manifest-cp114.json` (all 143 hashes), the scoped adapter and the *single* shared `pumlsc-shared.sty`. It must **not** commit licensed Times New Roman fonts, analysis workbooks, or research figure binaries.

From a fresh Git checkout:

```bash
python3 researchers/saugat-paneru/latex/scripts/restore_cp114_assets.py \
  --source-zip /private/path/CP114_FINAL_TNR_SOURCE__20261007.zip
cd researchers/saugat-paneru/latex/manuscript
./build.sh production
```

Restoration requires the exact originally accepted ZIP SHA and each individual asset hash; existing mutated files cause a hard failure. `build.sh` checks that all 143 required assets are in place before any LaTeX work.

## Unfinished release gates

- Official university/supervisor formatting acceptance and full 144-rule compliance: **HOLD**.
- New scientific CURRENT promotion and thesis Git tag/release: **NOT PERFORMED**; CP114 remains accepted.
- Scientific debts (EQx/EQy source provenance, nonlinear pushover/hinge controls, unmatched four-storey data): unchanged.

**Versioning:** This update closes source packaging, Drive custody and technical reproducibility tasks; it does not rewrite scientific evidence, claim final university approval, or retroactively close historical A9 acknowledgements.
