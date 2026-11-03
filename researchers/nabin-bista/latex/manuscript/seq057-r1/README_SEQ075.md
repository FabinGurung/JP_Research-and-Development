# Nabin Bista — LATEX_SEQ075

Complete source for the 121-page thesis PDF. Base: verified permanent Drive SEQ071.
This recovery completes the requested figure and table replacements after the earlier
local-only SEQ072–074 attempts. Their labels and history have not been overwritten.

## Build

Install the owner-licensed Times New Roman faces privately. Use an installed
TeX Live/XeLaTeX, bibtex8 and xdvipdfmx, then run:

```bash
bash build_seq075.sh
```

The build loads the exact pinned central style from `controls/latex/template/`.
It uses the existing `ieeetr` bibliography selection and all original scientific
assets. No font files are distributed. The PDF is delivered separately.

## Scope and restoration

See `SEQ075_A7_SCOPED_RELEASE.json` and `SEQ075_BUILD_AND_SCOPE_QA.json`.
The original RAR and schematic images are preserved in the dedicated Drive source
folder. All 18 replacement plot PNGs and both schematic JPEGs are included unchanged.
Only four manuscript `.tex` files differ from SEQ071, including the necessary
central-style compatibility repair. All original scientific binary assets and
bibliographic sources are preserved. No independent ETABS/fragility analysis or
supervisor approval is claimed. Final provider/Git evidence is in the external
000018 release receipt; it is not printed in the academic manuscript.
