# Structural Analysis and Design Report — draft candidate

**Ownership:** Enterprise Documents owns the TeX layout and PDF renderer. The independent solver algorithms, structural canonical model, code checks, regression tests, and benchmark comparators belong in [JP Structural Analysis](https://github.com/FabinGurung/JP_Structural_Analysis). A7 is a read-only catalogue and must not be edited by this module.

This is an additional **candidate template**, not an implicit modification of the currently authoritative 14 document types. Do not use it for certified construction reports until technical design modules and approvals exist.

## Compile the fictional example

```sh
python3 scripts/document_engineering/build_structural_report.py --input examples/document-engineering/structural-report.fictional.json --out /tmp/sar-demo --compile
```

Requires Python 3 and pdflatex. Private report inputs must stay in authenticated private storage, never public CI/logs. The shipped fixture is fictional.

## Input and result contract

Every claimed result has a status (HOLD, SOLVER_RESULT_UNCHECKED, UNVERIFIED_SOURCE_CLAIM or VALIDATED_WITH_EVIDENCE). Validation status is **not a self-attestation**: the renderer rejects that status unless result ID, analysis run ID, model SHA-256, source authority ID and external validation ID are present. Presence of IDs is necessary but **not sufficient** for engineering approval.

Typical families: introduction; general features; geometry; materials/covers; load cases and combinations; seismic spectrum/period/base shear; modal mass; member force diagrams; storey displacement and drift; torsion/soft storey/mass irregularity; reactions; column/beam/slab/footing/stair design; verification; appended calculations and provenance.

The precedent DOCX and revised PDF remain private. Their client names, personal contacts, existing table numbers, copied images and third-party figures must not be moved to public GitHub. Report precedent describes ETABS frame analysis, SAFE foundations and spreadsheet slab/stair calculations. **No E2K dependence is mandated**: new analyses should start from an independently authored canonical model.

## Current limitation

This is an executable draft **layout**, not yet a complete 68-page report recreation and not a certified independent design. External reviewer acceptance, code-edition checks, dimensional verification, numerical solver tests, source data alignment and visual QA are independent gates.
