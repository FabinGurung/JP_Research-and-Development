# CP113 Supervisor Corrections QA — 2026-10-06

Parent authority: CP112R2 (`CP-20261005__CP112R2_MODAL_MASS_PARTICIPATION_TNR_RELEASE`).

Implemented correction set:
- Table 4.11: removed the unavailable EQy maximum column; retained Model, Max. EQx ULS storey shear, and Governing available case.
- Literature Review: added an original, reproducible schematic of seismic vulnerability of low-rise RC buildings. The figure is conceptual and literature-grounded; it is not a new analysis result or fragility curve.
- Literature Review ordering: Summary of Literature Review now precedes Research Gap (auto-numbered 2.17 and 2.18 in this build).
- Figure captions: simplified to human-readable thesis captions; internal/AI/machine naming removed from submission-facing captions.
- Interpretation: explicit interpretation paragraphs added for the newly generated/self-created conceptual and comparative figures touched by this correction set.
- Figure 2.1 is now the vulnerability schematic; the prior pushover-concepts figure is renumbered by LaTeX as Figure 2.2.

Vulnerability-figure policy:
- Preferred: original schematic synthesized from cited literature and clearly identified as conceptual.
- Reproduction of an external published figure requires a reuse licence/permission where applicable; citation alone is not a blanket copyright permission.
- An adapted/redrawn schematic should cite the intellectual sources and must not imply that source data were measured in this thesis.

Preview build boundary:
- Runtime does not contain the private exact Times New Roman production cache used for CP112R2.
- Preview therefore uses Tinos fallback only for QA. It is NOT an exact-TNR production release and must not supersede CP112R2 CURRENT on that basis.

Preview compile QA:
- 115 A4 pages.
- XeLaTeX/Biber stabilization completed.
- LaTeX/package errors: 0.
- Undefined references/citations: 0.
- Overfull hbox/vbox: 0.
- Oversized floats: 0 detected.
- Biber warnings: 0.
- Visual spot QA: literature vulnerability page, pushover-concepts page, and Table 4.11 page render legibly without clipping.

Release status: CANDIDATE / SOURCE-CORRECTED / EXACT-TNR PRODUCTION PENDING.
