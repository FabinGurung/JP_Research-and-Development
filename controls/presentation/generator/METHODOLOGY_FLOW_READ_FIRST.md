# Read first — methodology flow

Use the current canonical shared code in GitHub `controls/presentation/generator/` and current academic Drive presentation tower before touching a researcher presentation. The `methodology_flow` slide defaults to a native editable 4:3 left-to-right six-stage flow. The researcher supplies process stages in structured JSON, linked to *their own* admitted manuscript/evidence IDs. The structural validator, semantic checker and PDF/PPTX renderer are shared. A researcher-specific candidate JSON alone is not a finished PPTX or scientific signoff.

1. Read `METHODOLOGY_FLOW_POLICY.md` and `methodology_flow.template.json`.
2. Confirm current researcher manuscript commit, version, Chapter 3 and admitted evidence map.
3. Author stages without inventing completion, sample size or measured findings.
4. Validate with `test_a9_methodology_flow.py` and the whole-deck test suite; inspect production renders.
5. Issue a *new* enumerated PPTX/PDF only after preview/approval and A9 PRE/POST/readback.
