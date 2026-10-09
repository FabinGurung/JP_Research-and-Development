# R&D thesis infrastructure — governed release checkpoint · 2026-10-09

**Status:** Shared infrastructure delivered and GitHub source validation passed; source package raw ZIP unavailable; individual Drive migrations, true thesis PDFs, 144-rule production certification, project ID resolution and A9 Local/Main registrations remain open.

**Main PRE:** `e33e4db6953f18ecacc9c3f0af537095c7ec144f`. Post-commit history is in `registry/thesis-infrastructure-run-log.json`. The exact live final SHA must be resolved from GitHub provider after the final push; never guess the self-referential commit.

## Actual deliverables

- `registry/researcher-folder-roles.json` — 11 RSH identities, 10 existing verified primary roots, 107 provider-read folder mappings; 004 Safal Thapa HOLD.
- `controls/researcher-folder-contract.json`, `schemas/researcher-folder-contract.schema.json` — persistent Drive-ID = identity, alias label = human descriptor.
- `scripts/researchers/normalize.py` — read-only planner, validator and local handover generator. `scripts/researchers/test_normalization.py` regression unit tests.
- `docs/researcher-normalization/RSH-001__folder_handover.md` through `RSH-011__folder_handover.md` — eleven individual governed instructions.
- `controls/latex/pu-rule-enforcement-matrix.json` — 144 original rules classified into planned template/Python/PDF/manual gates with all universal certifications on HOLD; no empty parity claims.
- `registry/latex-build-profiles.json`, `scripts/latex/universal_preflight.py`, `scripts/latex/pdf_technical_qa.py`, `scripts/latex/universal_compile.py`, `docs/UNIVERSAL_THESIS_BUILD_READ_FIRST_20261009.md` — real generic runner with explicit project approval. No PDF compiled during central normalization.
- `.github/workflows/researcher-source-gates.yml` — paths-restricted source gate, no automatic scientific PDF/Drive upload.
- Live `/thesis-infrastructure/` researcher role directory, individual researcher page additions and copied machine-readable role data.

## Provider checks and ownership

Google Drive original PU v1.13, Thesis Tower v1.23, Save Router v1.13 and Main A9 provider-read. Main `POST__LocalLibraryRegistry__39` reports the historic Safal seq2 ACK; separate Safal Local SyncState seq17 / Main cursor5 HOLD. No cursor was advanced.

No folder renaming/moving/deleting/creation; no researcher scientific content touched. Historical Git branches, tags and releases preserved. Git nonforced PRE/POST only; no new snapshot branches. No A9 ArtifactRegistry/ArtifactEdges/VersionLog/RunLog mutation claimed: this Git run log is a pending bridge and owning A9 registration must be executed separately.

**Unresolved:** named ZIP raw package was unavailable; actual project IDs not independently verified; ten researchers' physical normalization and RSH-004 root discovery remain owner-scoped; PU 144-rule rendered format parity and generic exact-font real-PDF tests remain open; manuscript release approvals and all A9 Main ACKs remain independent.

For per-researcher work, use its `RSH-XXX__folder_handover.md`, fresh-resolve Drive IDs, and apply owning A9 PRE/POST.
