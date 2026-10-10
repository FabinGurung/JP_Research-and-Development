# A9 Presentation — Scientific Semantic Validation (Candidate v0.1)

Status: **CANDIDATE / NOT PROMOTED**. Compatible with the Drive v2.2 presentation tower and generator v2.1; does not replace them. No researcher data or licensed fonts included.

`a9_semantic_checker.py` enforces machine-verifiable **provenance linkage**, not scientific truth. No automated system can validate claims from a photograph alone. Researcher and supervisor admission/review remain mandatory.

## Researcher contract

The researcher JSON content sets `metadata.project_id` and each slide's `scientific_role` from `BACKGROUND`, `METHOD`, `OBSERVATION`, `RESULT`, `INTERPRETATION`, `RECOMMENDATION`, `LIMITATION`, `NON_SCIENTIFIC`.

An external private `evidence_map.json` identifies the same project, source commit and source manifest ID, and lists project-only `sources[]` with IDs and explicit `admission_status` (`ADMITTED_CURRENT` or `APPROVED_CURRENT` to be usable). Slides cite `evidence_refs[]`; empirical observations/results/interpretations require `admission_decision_id`, recommendations also require `recommendation_basis`. A candidate, rejected, superseded, or missing source is a **release blocker**.

Examples use non-scientific synthetic data only. **Never copy a historical Safal deck's result/numerical claim into the current deck without a current evidence decision.** Private photo locations are not public Git material.

## Run

```sh
python -m unittest -v test_a9_semantic_checker.py
python smoke_test.py
python build.py --content researcher-content.json --evidence-map private/evidence_map.json --theme theme.default.json --out-dir build
```

`python build.py ... --fixture` is strictly a synthetic test pathway and the release manifest labels it `FIXTURE_ONLY`. `--production` is forbidden with `--fixture`. Independent exact Times New Roman and full visual QA remain required.

## Known limitations / must not overclaim

- `scientific_role` and evidence IDs can be fabricated in JSON; metadata checks cannot establish authenticity of the underlying source or supervisor approval.
- Heuristic title/quantity cues only produce prompts for inspection, not exhaustive science validation.
- Existing geometry validator is basic; `a9_render_qa` still reports `visual_status = REQUIRES_HUMAN_OR_MODEL_RENDER_REVIEW` and does not certify all-slide visual QC automatically.
- Current Drive release cannot be labeled as including this checker until properly versioned, reviewed and registered.
