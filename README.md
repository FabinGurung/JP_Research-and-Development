# JP Research & Development

Code-first research control portal.

## Current field

This repository stores **code, machine-readable controls, version history, and Google Drive/GitHub pointers**. It does not store working research documents or generated binaries on `main`.

- **Google Drive:** actual working documents, discussion Google Docs, compiled thesis PDFs, generated presentation PPTX/PDF, datasets/evidence when appropriate.
- **GitHub main:** public portal source, researcher index, shared Discussion/LaTeX/Presentation controls, schemas, scripts, and links.
- **Researcher lanes:** `researcher/<slug>/discussion`, `researcher/<slug>/latex`, `researcher/<slug>/presentation`.
- **GitHub Pages:** human-facing researcher/control workspace.
- **GitHub Actions:** validates the repository policy and deploys `main` only.

All nine researcher pages are currently **ON HOLD — HUMAN QA REQUIRED**. Topic titles and Drive IDs remain null until explicitly verified.

## Live site

https://fabingurung.github.io/JP_Research-and-Development/

## Shared controls

- `controls/discussion.control.json`
- `controls/latex.control.json`
- `controls/presentation.control.json`
- `controls/repository.control.json`

## Minimal versioning rule

For Git-managed state, the previous commit SHA is PRE and the new commit SHA is POST. Git history is the archive. Do not manufacture duplicate Drive PRE/POST copies or acknowledgement-only commits. Provider readback remains required for external Drive links and production deployment.

## Build

```bash
python scripts/validate_repo.py
python scripts/build_site.py --out dist
python scripts/validate_repo.py --site dist
```
