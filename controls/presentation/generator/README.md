# A9 + PU MSc Presentation Generator v2.1

Executable generalized presentation source package for A9 Presentation Control v2.2.

## Canonical flow
structured JSON content + governed assets -> validation -> deterministic PDF -> per-page render QA -> montage -> optional PPTX compatibility export.

## v2.1 changes
- Title-slide institutional logo default/minimum is **2.25 in**, greater than 2x the previous 1.00 in project baseline.
- The canonical institutional logo is aspect-ratio preserved and is validated before release.
- Verified Supervisor name is compulsory on the title slide when available.
- Every verified Co-Supervisor / Sub-Supervisor is compulsory when available.
- Generic schema/validator/renderer support is provided; researcher-specific identities remain project-local.

## Files
- `build.py` — orchestration entry point.
- `a9_presentation_validator.py` — client-facing/source/asset/title-metadata validation.
- `a9_presentation_generator.py` — fixed-layout PDF and PPTX rendering.
- `a9_render_qa.py` — raw PDF-page rendering, hashes and montage.
- `theme.default.json` — 4:3 geometry, 2.25 in title-logo gate, typography floors, black-on-white academic visual language.
- `presentation_schema.json` — structured content contract including supervisor metadata.
- `content.example.json` — non-scientific smoke-test content.
- `requirements.lock.txt` / `environment.lock.json` — pinned environment.
- `smoke_test.py` — deterministic executable acceptance test.

## Build
```bash
python smoke_test.py
python build.py --content content.example.json --theme theme.default.json --out-dir build
```

Use `--production` only when exact Times New Roman is installed and production requirements are independently verified. Otherwise outputs are preview/non-production.

## Researcher integration
Never populate from an older presentation. Resolve current researcher/project CURRENT/source manifest, canonical PU logo, verified supervisor/co-supervisor metadata and admitted evidence first. Keep researcher content and identities in project-local structured content.
