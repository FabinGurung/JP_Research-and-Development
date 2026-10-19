# Modal mass participation data pipeline

Authority snapshot: seven model workbooks copied from the user-provided `Mass participation Ratio` Drive folder on 2026-10-04.

Inputs:
- `data/modal_mass_participation/*.xlsx`
- Worksheet: `Modal Participating Mass Ratios`

Normalized output:
- `generated/data/modal_mass_participation_tidy.csv` (7 models × 5 source blocks × 12 modes = 420 rows)
- `generated/data/modal_mass_participation_z040_type_c_summary.csv`

LaTeX outputs:
- `generated/tables/modal_extraction_fields.tex`
- `generated/tables/modal_period_mass_z040_type_c.tex`
- `generated/tables/modal_cumulative_mass_z040_type_c.tex`

Printed comparison basis:
- Soil Type C, Z=0.40, matching the principal seven-model response comparison in Chapter 4.

The `.tex` tables are generated artifacts. The XLSX copies are the local source snapshot; do not edit generated values by hand.
