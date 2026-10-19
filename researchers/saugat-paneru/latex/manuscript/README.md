# Saugat Paneru — Git LaTeX source migration (CP114 content parent)

- Canonical shared academic style: [`controls/latex/template/pumlsc-shared.sty`](../../../../controls/latex/template/pumlsc-shared.sty). **Do not copy or fork that style.**
- The CP114 **scientific text and bibliography** are imported verbatim from [Drive source ZIP](https://drive.google.com/file/d/1yL3G-EUGA32FDBhkdImXk9NManfW_vyA/view). Only `main.tex` uses `pumlsc-shared` instead of the old full-format style.
- `saugat_project_adapter.sty` bridges only CP114-specific metadata/front pages/list structures unavailable in the current partial shared template, not a second canonical university style. `saugat_compat.sty` contains researcher package imports and project-specific source aliases.
- Figures, architectural plans, hinge images, original XLSX and licensed font binaries **do not live in public Git**. Obtain the verified source archive from Drive and run `python3 scripts/restore_assets.py --source-zip /path/to/CP114_FINAL_TNR_SOURCE__20261007.zip` to restore checksummed assets locally.
- Build with `./build.sh production` only where authorized exact Times New Roman is installed as a private dependency; Tinos `preview` is not production.
- Current official Drive release remains CP114 (115 A4 pages). Any new Git template PDF must pass independent machine/render QA before a new release is promoted. Reflow and project-specific template exceptions are tracked; no scientific values were re-derived.
- Old Project Local global51 / Main49 remains a **historical unacknowledged** boundary, not an acceptable inferred Main ACK. Oct 11 scoped Git/Drive cutover governs *new* Git version commits.
- Missing EQy / pushover/height provenance is held as described by CP114, not a blocker to exact-content source migration and not permission to invent results.
