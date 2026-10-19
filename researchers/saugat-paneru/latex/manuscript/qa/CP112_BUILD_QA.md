# CP112 Candidate — Machine Build QA

- Compile route: XeLaTeX -> Biber -> XeLaTeX stabilization.
- Main font: exact Times New Roman production faces loaded; no fallback warning.
- Output: 112 A4 pages.
- TeX errors: 0.
- Undefined citations: 0.
- Undefined references: 0.
- Overfull hbox: 0.
- Overfull vbox: 0.
- Oversized-float warnings: 0.
- Rerun/cross-reference warnings: 0.
- Biber warnings: 0 after month-field normalization.
- Remaining non-blocking warning: `caption` reports unused plate-specific caption setup because plates are disabled in this build.
- PDF post-editing: none; PDF is generated from LaTeX source.
- Visual QA: explicitly deferred to the user and is not marked PASS.
- Seven clean model-plan PDFs: byte-identical to the verified source files; embedded as PDF/vector inputs.
- Data recomputation: PASS for Modal T1 / reported 90%-criterion mode-period, complete C/Z=0.40 drift profiles and maxima, EQx Story-1 shear, main-storey CM-CR maxima, and performance-point maxima.
- Fail-closed omissions retained: T2/T3 and numeric X/Y modal mass participation; EQy storey-shear series; member-level critical hinge table; exact control-node/target-displacement/step/gravity-sequence fields not available in the retained analysis records.
