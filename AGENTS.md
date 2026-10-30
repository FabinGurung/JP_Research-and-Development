# JP R&D — agent entrypoint

**MANDATORY R&D READ FIRST:** [Memory Wall](docs/MEMORY_WALL.md) and [LaTeX template inheritance/versioning](docs/LATEX_TEMPLATE_INHERITANCE_VERSIONING.md). Read latest `main` and current researcher Drive source/manifest. For new thesis source versions, prefer the dry-run-first [per-researcher sequence reservation](.github/workflows/latex-reserve-researcher-sequence.yml), pin the exact central template SHA, and keep scientist source paths isolated. Never confuse Git revision, scientific CP, global `RD-LTX-CHG` IDs, or stable Drive PDFs. This governs only this R&D repository; A7 remains a read-only catalogue.

Read the authoritative, public-safe cross-provider bootstrap from **A7** before multi-repository work:
https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/blob/main/A9_GIT_DRIVE_BOOTSTRAP.json

Then resolve this module's `A7_MODULE.json`, current `CURRENT.json` and only the exact researcher/project control needed. Git tracks entire repository source history. Researcher folders share the main website codebase; named researcher branches are optional work/compatibility refs, not isolated databases. Compiled PDFs/PPTX and research originals remain in Google Drive. Do not copy private A9 documents into public GitHub. Historical A9 constraints remain in force for not-yet-reconciled Drive workflows.

## Single LaTeX authority
For ANY thesis LaTeX preparation read `controls/latex/tower.json` and load **only** `controls/latex/template/pumlsc-shared.sty` as shared template. `controls/latex.control.json` is a routing alias. All 11 researcher entries inherit one shared control via `registry/latex-inheritance.json`; any researcher-origin visual/template fix must enter `controls/latex/change-register.json` as an ID >=101, then either update shared source after QA or register a researcher-only delta in `controls/latex/extension-registry.json`. A7 has no LaTeX control tower. Do not publish private data or fonts.

## Binding approved 2026-10-09 rules (Q1B Q2A Q3A)
Git `main` PRE/POST is the release history; do not create routine branches for snapshots. Use **annotated tags** only for accepted major releases via a supported tag-capable interface. Historical 106 refs are immutable until separately audited. `controls/latex/pu-format-parity-audit.json` maps 144/144 PU v1.13 source rules; source mapping is not a rendered production PDF certificate. Safal latest is v1.9 Local seq15 (Q1 B), pending provider byte verification before manuscript admission, not the old v1.2 or first uploaded v1.9 bytes. Public R&D Git may contain verified academic source `.tex` and `.bib`; do not insert artificial workflow/control text into research prose or invent evidence.

## Enterprise Document Engineering v2 (2026-10-10)
One enterprise tower: `controls/document-engineering/tower.json`; fourteen type modules under `controls/document-engineering/types/`; shared DRAFT style `templates/enterprise/v2/enterprise-shared.sty`; renderer `scripts/document_engineering/engine_v2.py`; semantics `controls/document-engineering/semantic-handrails.v2.json`. Original Overleaf ZIP and sensitive data remain private in A9 Drive. Passing source checks or compiling a PDF never authorizes legal, technical, HR, financial approval or signatures. Do not use the older three prototype templates as production authority. The original Radha Roka contract is a failed working candidate; preserve it only for rollback and critique. The academic LaTeX tower is separate.

## A7 is a READ-ONLY CATALOGUE for this repository

Treat the A7 system registry as a read-only metadata directory and knowledge-graph pointer index for this module. **NEVER write A7 files, branches, PRs, website code, schema/policy templates, catalogue rows or histories during this repository's tasks.** A module task is not authorization for A7 work, even if its link appears stale. Create a local pending pointer-correction note and request a **separate explicit A7-specific instruction**. Actual execution logic, internal schemas, templates, publishing and version history belong in this repository and its declared owner providers. The historical A7-hosted AI-Aided Design guidance is not the CAD template authority; CAD's versioned canonical template lives at `FabinGurung/JP_Computer-Aided-Drawings/governance/aad/aad-domain-template.v0.1.json`. Do not modify CAD unless that separate domain is tasked. Preserve all existing governance, privacy and branch rules above.

## All-researcher engine enrollment (2026-10-30)
Every enrolled researcher has `researchers/<slug>/AGENTS.md`. Read
`docs/RESEARCHER_ENGINE_READ_FIRST.md` on fresh main before resuming. Enrollment
is governance routing only; it is not sequence-baseline verification, manuscript
rewriting, a template-pin upgrade, or scientific/PDF approval.
