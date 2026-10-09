# JP Research & Development

Code-first research control portal, now hosting unified Fabin AEC and Hydropower research landing pages and restored public-safe legacy demos.

## Current field

This repository stores **code, machine-readable controls, version history, and Google Drive/GitHub pointers**. It permits verified research manuscript source `.tex`, `.bib` and related code on `main`; compiled PDFs/PPTX and binary research evidence remain versioned in Drive.

- **Google Drive:** actual working documents, discussion Google Docs, compiled thesis PDFs, generated presentation PPTX/PDF, datasets/evidence when appropriate.
- **GitHub main:** manuscript source code, reusable LaTeX template, research registry, controls, schemas, scripts and project links.
- **Universal researcher lanes:** `researcher/<slug>/discussion`, `researcher/<slug>/latex`, `researcher/<slug>/presentation`.
- **Optional website modules:** `researcher/<slug>/website/<module-slug>` only when a real web module is verified or explicitly started. Currently verified: Fabin AEC and Fabin Hydropower/PhD.
- **GitHub Pages:** human-facing researcher/control workspace.
- **GitHub Actions:** validates the repository policy and deploys `main` only.

Researcher metadata is admitted incrementally through live Drive evidence and human QA. The current registry contains **11 distinct researcher identities** and **33 core researcher lanes**. Safal Dawadi (RSH-010; MSc Construction Management) and Safal Thapa (RSH-004) are separate people and must never be conflated. Sunil Rana is RSH-011. Some manuscripts, Discussion/Presentation outputs, scientific source admissions, and final approvals remain on explicitly registered holds. The direct-child `02_Thesis` Drive audit covers all 18 currently observed folders; the folder audit is not itself scientific submission approval. Existing optional website modules remain separate.

## Live site

https://fabingurung.github.io/JP_Research-and-Development/

## Shared controls

- `controls/discussion.control.json`
- **ONE canonical LaTeX manuscript tower and shared template:** [`controls/latex/tower.json`](controls/latex/tower.json) → [`controls/latex/template/pumlsc-shared.sty`](controls/latex/template/pumlsc-shared.sty). Legacy `controls/latex.control.json` is only a route alias.
- `controls/presentation.control.json`
- `controls/repository.control.json`

## Minimal versioning rule

For Git-managed state, the previous commit SHA is PRE and the new commit SHA is POST. Git history is the archive. **Q2 A:** no routine snapshot branches; use annotated tags for major accepted releases once supported, preserving existing historical refs. Archived branch refs are also physically namespaced under `archive/`.

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

## Source branch directory · Rose Dawn UI (v001)

- All GitHub branches, categorized by actual purpose and observed SHA: [published branch directory](https://fabingurung.github.io/JP_Research-and-Development/branches/)
- Machine inventory: [registry/branch-inventory.json](registry/branch-inventory.json)
- Naming, snapshot and rollback rule: [docs/BRANCH_VERSIONING_AND_INVENTORY.md](docs/BRANCH_VERSIONING_AND_INVENTORY.md)
- Theme: [docs/PORTAL_THEME.md](docs/PORTAL_THEME.md) — default rose dawn, optional mauve dusk; legacy demos unmodified.

Do not infer the 33 named researcher branches contain their final thesis sources: they currently share a previous template code baseline. New `resource/**/v001-20261009` refs include the updated full repository code and scoped manifests. Git history gives rollback by exact SHA; enumerated dated snapshots preserve major boundaries without repeated Drive copies.

## Dated immutable rollback snapshots

- PRE: [v001 before Rose Dawn](https://github.com/FabinGurung/JP_Research-and-Development/tree/snapshot/20261009/rnd-main/v001-pre-rose-dawn)
- POST: [v002 after UI and branch page](https://github.com/FabinGurung/JP_Research-and-Development/tree/snapshot/20261009/rnd-main/v002-post-rose-dawn-and-branches)

101 observed refs include 14 new source-resource branches and two descriptive legacy aliases; previous branches remain untouched. Git commit SHA is the exact rollback coordinate. The v002 snapshot is immutable; this metadata update advances `main` beyond it.

## Safal Dawadi scoped LaTeX control

The [public control page](https://fabingurung.github.io/JP_Research-and-Development/controls/latex/safal-dawadi/) and [machine project config](controls/projects/safal-dawadi.latex.json) are governed by [shared LaTeX control](controls/latex.control.json). A7 owns global routing; original private Drive PU/A9 records own format/science. Three existing lanes are legacy template refs; source and PDF compilation remain held pending byte reconciliation and public privacy clearance. See [ownership runbook](docs/LATEX_CONTROL_OWNERSHIP.md).

## Q1B/Q2A/Q3A approval — 2026-10-09

- [144/144 live PU formatting rule IDs audited (production QA incomplete)](controls/latex/pu-format-parity-audit.json).
- [Safal v1.9 Local seq15 target](researchers/safal-dawadi/latex/source-baseline.json), with same-ID final source/PDF mirror/hash still pending, so Git source import has not yet occurred.
- [Git commits PRE/POST + annotated-tag-only major releases](docs/LATEX_Q1B_Q2A_Q3A_GOVERNED_CHANGE_20261009.md). Existing 106 refs remain stable. Admitted manuscript `.tex` and `.bib` may reside in this R&D repository.

**Safal runnable Linux handover:** [Read the current source-reconciliation, single-template, preview/production build procedure](docs/HANDOVER_SAFAL_DAWADI_LATEX_EXECUTION_20261009.md). A successful GitHub source gate is not a generated PDF.

## Thesis-wide normalized folder and document infrastructure (2026-10-09)

- **[Human navigation: researcher folder roles](https://fabingurung.github.io/JP_Research-and-Development/thesis-infrastructure/)** — 11 registered, ten verified roots; RSH-004 HOLD; immutable Drive identities and alias proposals.
- [Machine-readable existing folder registry](registry/researcher-folder-roles.json), [canonical logical folder contract](controls/researcher-folder-contract.json), [schema](schemas/researcher-folder-contract.schema.json), [gap matrix](docs/THESIS_FOLDER_NORMALIZATION_GAP_MATRIX_20261009.md).
- [Read-only folder planner and handover generator](scripts/researchers/normalize.py) and [11 individualized handovers](docs/researcher-normalization/). No centralized Drive mass migration.
- [Universal LaTeX source preflight](scripts/latex/universal_preflight.py), [PDF technical inspector](scripts/latex/pdf_technical_qa.py), [11 non-autonomous project profiles](registry/latex-build-profiles.json), [144-rule route ledger](controls/latex/pu-rule-enforcement-matrix.json).
- [Path-scoped source gates](.github/workflows/researcher-source-gates.yml) do NOT generate scientific PDFs. Full university production parity and A9 Main approval remain separate HOLDs.

- [Authorized XeLaTeX/Biber generic compiler](scripts/latex/universal_compile.py) and [build procedure](docs/UNIVERSAL_THESIS_BUILD_READ_FIRST_20261009.md): dry run by default; real PDF only on explicit owning project authorization.
- [Governed infrastructure checkpoint](docs/THESIS_INFRASTRUCTURE_RELEASE_20261009.md) and [Git lineage](registry/thesis-infrastructure-run-log.json). This is NOT an A9 Main ACK or a 144-rule PDF certificate.

## Living Research Library v2 and owner-only migration handovers

The [illustrated homepage](https://fabingurung.github.io/JP_Research-and-Development/) now has a self-contained, CSS-animated winged book, parchment/forest day theme, optional dark reading room, pause/reduced-motion support. It requires **no Three.js dependency**, remote images, or licensed fonts. Older standalone demos remain unchanged.

The [11 fully resolved researcher prompts](prompts/researchers/) are inert in GitHub: **only pasting the correct one into its owner's original researcher chat activates that owner's bounded, non-destructive migration**. All prompts inherit [central zero-delete migration rules](controls/researcher-migration-rules.json) and reproduce from [one master](prompts/researcher_owner_execution_master.md) using [the generation checker](scripts/researchers/generate_prompts.py). The [initial migration-status registry](registry/researcher-migration-status.json) has no started owner runs. RSH-004 has no verified Drive root and remains READ-ONLY HOLD. No automatic A9 Main ACK.

### Copy individual handovers directly from the website

[Open the 11-researcher handover reading desk](https://fabingurung.github.io/JP_Research-and-Development/owner-prompts/) to choose one researcher and use **Copy entire prompt**. Copying does not execute any operation; only you pasting it into that researcher's owning chat triggers a bounded governed procedure. [Schema](schemas/researcher-migration-status.schema.json) · [Release and design record](docs/OWNER_HANDOVERS_AND_LIBRARY_THEME_V2_20261009.md).
