# JP Research & Development

Code-first research control portal, now hosting unified Fabin AEC and Hydropower research landing pages and restored public-safe legacy demos.

## Current field

This repository stores **code, machine-readable controls, version history, and Google Drive/GitHub pointers**. It does not store working research documents or generated binaries on `main`.

- **Google Drive:** actual working documents, discussion Google Docs, compiled thesis PDFs, generated presentation PPTX/PDF, datasets/evidence when appropriate.
- **GitHub main:** public portal source, researcher index, shared Discussion/LaTeX/Presentation controls, schemas, scripts, and links.
- **Universal researcher lanes:** `researcher/<slug>/discussion`, `researcher/<slug>/latex`, `researcher/<slug>/presentation`.
- **Optional website modules:** `researcher/<slug>/website/<module-slug>` only when a real web module is verified or explicitly started. Currently verified: Fabin AEC and Fabin Hydropower/PhD.
- **GitHub Pages:** human-facing researcher/control workspace.
- **GitHub Actions:** validates the repository policy and deploys `main` only.

Researcher metadata is admitted incrementally through live Drive evidence and human QA. The current registry contains **11 distinct researcher identities** and **33 core researcher lanes**. Safal Dawadi (RSH-010; MSc Construction Management) and Safal Thapa (RSH-004) are separate people and must never be conflated. Sunil Rana is RSH-011. Some manuscripts, Discussion/Presentation outputs, scientific source admissions, and final approvals remain on explicitly registered holds. The direct-child `02_Thesis` Drive audit covers all 18 currently observed folders; the folder audit is not itself scientific submission approval. Existing optional website modules remain separate.

## Live site

https://fabingurung.github.io/JP_Research-and-Development/

## Shared controls

- `controls/discussion.control.json`
- `controls/latex.control.json`
- `controls/presentation.control.json`
- `controls/repository.control.json`

## Minimal versioning rule

For Git-managed state, the previous commit SHA is PRE and the new commit SHA is POST. Git history is the archive. Archived branch refs are also physically namespaced under `archive/`.

Governed research debt is tracked in `registry/debts.json` and projected to the live `/debts/` page. Researcher-scoped debt may also appear under that researcher’s workspace. Do not manufacture duplicate Drive PRE/POST copies or acknowledgement-only commits. Provider readback remains required for external Drive links and production deployment.

## Build

```bash
python scripts/validate_repo.py
python scripts/build_site.py --out dist
python scripts/validate_repo.py --site dist
```

## Unified research websites (2026-10-09)

- Fabin AEC / MSc Structural Engineering: `/researchers/fabin-gurung/websites/aec/`
- Fabin Hydropower / PhD: `/researchers/fabin-gurung/websites/hydropower-phd/`
- Hydropower proposal defense: `/researchers/fabin-gurung/websites/hydropower-phd/proposal-defense/`
- Interactive historical demos: `/methodology-demo/`, `/hydropower-nepal-map/`, `/hydropower-data-schema/`, `/hydropower-data-tables/`, `/hydropower-data-graph/`.

The static demos are reused from archived code blobs, not a claim that all archived Next.js pages were migrated. A researcher-specific Git branch snapshots the whole repository; the primary site is one build from `main`. [A7 single bootstrap](https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/blob/main/A9_GIT_DRIVE_BOOTSTRAP.json).

## Current roadmap and A7 handover (2026-10-09)

- **Live roadmap:** https://fabingurung.github.io/JP_Research-and-Development/roadmap/
- **Editable source:** [registry/roadmap.json](registry/roadmap.json), [docs/ROADMAP.md](docs/ROADMAP.md)
- **A7 cross-chat handover:** [docs/HANDOVER_TO_A7_20261009.md](docs/HANDOVER_TO_A7_20261009.md)
- **Global A7 roadmap:** https://fabingurung.github.io/JP_A7_System_Registry_and_Knowledge_Graph/roadmap.html

The roadmap distinguishes delivered work, scientific holds, Git source admission still pending, and private A9 library migration **not yet performed**. Do not treat the public site as scientific or private Main Library authority.
