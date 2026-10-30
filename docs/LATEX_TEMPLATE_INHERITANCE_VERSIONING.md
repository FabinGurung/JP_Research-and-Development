# LaTeX inheritance and independent researcher sequencing — PROPOSED v0.1

This is the detailed procedure linked by [R&D Memory Wall](MEMORY_WALL.md). It is NOT yet implemented as an automatic allocator or source gate. Reuse existing [single LaTeX tower](../controls/latex/tower.json), [inheritance registry](../registry/latex-inheritance.json) and [change register](../controls/latex/change-register.json), instead of creating an alternate control.

## Core architecture

~~~text
                           GitHub main
                              |
          +-------------------+-------------------+
          |                                       |
  ONE shared PU style                       Registry + CI
  controls/latex/template/                  inheritance, versions,
  pumlsc-shared.sty                         amendments and releases
          |                                       |
          +--------------+------------------------+
                         |
        New work branches start from latest approved main
                         |
          +--------------+----------------+
          |                               |
 thesis/saugat-paneru/...        thesis/nabin-bista/...
          |                               |
 manuscript + private adapter    manuscript + private adapter
          |                               |
 independent CP/evidence         independent CP/evidence
          +--------------+----------------+
                         |
          scoped researcher PRs → accepted main
                         |
            individual PDF/source/QA builds
                         |
          Drive custody + SHA and CURRENT pointer

 Proven general formatting defect on a researcher branch
    → GLOBAL_CANDIDATE PR → multi-researcher regression
    → template version bump → merge into one main style
    → next new researcher branch inherits that new style
~~~

## Version and file ownership boundaries

- **One template source only:** `controls/latex/template/pumlsc-shared.sty`. All researchers reference it by canonical path; **never duplicate** it under an owning manuscript.
- **One machine tower:** `controls/latex/tower.json`. Its existing modules are subordinate, not rival towers.
- **Per-researcher source:** `researchers/<slug>/latex/manuscript/**` and properly registered `extensions/**`.
- **Per-researcher release manifest:** `researchers/<slug>/latex/production-current.json` or current governing manifest; do not infer a universal identical filename when a researcher has a different admitted source layout. A future standardized interface can map their existing manifests without destroying history.
- **Scientific model + raw evidence:** original controlled files in Drive, by exact source ID and SHA. No cross-researcher copying.
- **Git shared-global changes:** restricted to independent format PRs; no single researcher can change global style as an invisible side effect of prose edits.

## How a fresh researcher branch obtains the current style

First read current researcher scientific and version manifests and the latest Git main SHA. When a numbered researcher sequence has been **properly reserved**, create from fresh main:

~~~bash
git fetch origin main
git switch -c thesis/<slug>/latex/seqNNN-<short-topic> origin/main
# Example *format only*; never assume a particular seqNNN is available.
# Edit only researchers/<slug>/latex/... and approved researcher metadata.
git add researchers/<slug>/latex/
git commit -m "thesis(<slug>): seqNNN <bounded change>"
git push -u origin thesis/<slug>/latex/seqNNN-<short-topic>
~~~

The repository working tree on that branch already contains the shared `controls/latex/template/pumlsc-shared.sty`; no extra copy or external Git submodule is needed. The researcher's build script or `TEXINPUTS` resolves that path. The branch records exact PRE `main` SHA and style SHA/version. A branch is a **whole-repository snapshot**, not a Git folder-only branch.

**Why not `researcher/<slug>/latex/seqNNN`?** Historical refs `researcher/<slug>/latex` already exist: Git cannot store both a leaf ref and child ref using the same prefix. The `thesis/` namespace avoids forcing deletion/rename of those historical branches.

## Proposed sequence reservation (not yet automated)

The next improvement should be a single append-only, per-researcher version register, e.g. `registry/researcher-latex-sequences.json` with explicit schema, entries and unique keys `(researcher_id, lane, sequence_number)`.

A reservation is an **atomic, serialized operation against latest main**:

1. Read current accepted and reserved sequence numbers; do not reuse or silently renumber historical LATEX_SEQ and M4 checkpoint labels.
2. Determine next genuinely free number in that researcher's own namespace. A visible GitHub issue/PR or task UUID owns the reservation; log parent Git SHA and original source/Drive CURRENT.
3. Acquire a researcher-scoped serialization gate, e.g. GitHub Actions concurrency `latex-sequence-<slug>`; compare-and-swap the expected parent SHA. If changed, re-read/retry (never force push).
4. Append reservation with status `RESERVED` and link to exact work branch. Abandoned reservations become `ABANDONED` with an explanation, never reused. No fictitious commits.
5. On accepted PR, set `MERGED` with actual Git POST SHA. On signed-off Drive deliverables, record `RELEASED` with Drive IDs, SHA and optional approved Git tag.
6. Gate source PRs against registered scope, unallocated or duplicate seq, expected template SHA and unrelated researcher edits.

Until this allocator is actually implemented and tested, **the maintainer checks the live sequence evidence and reserves the next number explicitly**. Do not promise an automated `seq055` or invent an Saugat sequence solely because a new chat opened.

## Proposed manifest fields for every new version

~~~json
{
  "researcher_id": "RSH-XXX",
  "lane": "latex",
  "sequence_number": "RESERVED_NUMERIC_VALUE",
  "branch": "thesis/<slug>/latex/seqNNN-<topic>",
  "scientific_checkpoint": "OWN_VERIFIED_CP",
  "source_pre_sha": "ACTUAL_MAIN_SHA",
  "source_post_sha": "ACTUAL_ACCEPTED_COMMIT_SHA_OR_NULL",
  "shared_template_path": "controls/latex/template/pumlsc-shared.sty",
  "shared_template_version": "VERIFIED_ACTUAL_VERSION",
  "shared_template_blob_sha": "ACTUAL_SOURCE_BLOB_SHA",
  "local_extension_ids": [],
  "admission_state": "CANDIDATE_OR_APPROVED",
  "pdf_drive_id": null,
  "pdf_sha256": null,
  "source_zip_drive_id": null,
  "source_zip_sha256": null,
  "qa_receipt": null,
  "approval_evidence": null
}
~~~

`null` explicitly means not yet produced or approved. Store actual IDs only after provider readback. Never place private material or licensed Times New Roman font binaries in public Git.

## How a scientist's finding becomes a better global template

| Situation | Where change belongs | Approval/tests |
|---|---|---|
| Nabin fixes a hospital-specific figure caption or analyses | Nabin-only manuscript | Scientific evidence, owning researcher |
| Saugat needs a special one-off page/figure arrangement | Saugat registered extension | Local before/after and stable shared-template import |
| Several researchers encounter an identical official PU margin/heading defect | One shared template `GLOBAL_CANDIDATE` PR | PU primary source, central amendment ID, cross-researcher builds where available, visual QA |
| Shared template gets a new optional helper | Central style, bump minor/patch according to compatibility | Existing users unaffected unless opted in; regression tests |
| Shared template intentionally changes a default | Central style, **major** migration planning | Explicit researcher version adoption, visual comparison and approval |

Global promotion: log `RD-LTX-CHG-NNN` using live `next_number`, mark `GLOBAL_CANDIDATE`, provide source and before/after evidence; amend canonical `.sty` and corresponding tower/rules; run `scripts/latex/validate_shared.py`, `scripts/latex/universal_preflight.py --policy-check`, source gates and all **available** researcher regression builds. On pass and approval, merge to `main`, bump style's semantic version and create a verified release tag when authorized. Mark superseded per-researcher extensions to avoid double application.

## Template adoption at a new versus ongoing revision

**New branch:** resolve style from the latest **approved** `main` at creation. Pin that exact style blob/commit in its manuscript-version manifest. This naturally picks up global improvements.

**Open/ongoing branch:** does not magically change when shared `main` updates. Explicitly pull/rebase/merge and record whether the template is upgraded. If build changes because of the new format, produce before/after page QA; if not ready, retain older pinned commit.

**Released thesis:** immutable semantic content and compiled PDF. A later global template change **never silently rebuilds or overwrites** older released PDFs. A new version is needed to adopt and publish the updated style.

## Protecting Nabin and Saugat during concurrency

- All PRs are scoped by changed path. Touching a second researcher scientific directory requires explicit multi-researcher authorization.
- Updating `registry/latex-inheritance.json` or a shared `controls/latex/**` path is a separate GLOBAL scope subject to central QA.
- If different researchers branch from the same `main`, their own file edits normally merge cleanly, but a shared register edit can conflict. Resolve with a fresh main read, rebase/merge, and re-run CI; do not overwrite either PR or skip validation.
- Protected `main`, required source checks, PR approvals and CODEOWNERS are recommended controls; verify actual GitHub repository settings before claiming them active.
- Do not depend on a long-lived leaf `researcher/<slug>/latex` legacy branch to supply current source. Always base an actual numbered branch on fresh `main`.

## Release/checkpoint lifecycle

`RESERVED → EDITING → CI_PASS → SCIENTIFIC_REVIEW → PDF_RENDER_QA → DRIVE_READBACK → CURRENT_PROMOTED → TAGGED_RELEASE`.

An intermediate state may be `HOLD`, `REJECTED`, `SUPERSEDED` or `ABANDONED` without deleting commits or evidence. Print-ready layout is not scientific authorization or signed university acceptance. Only a specifically authorized release may advance the stable Drive CURRENT pointer. A template-only update does not manufacture a new scientific CP.

## Adoption tasks (future implementation, not yet done)

1. Approve this principle and reconcile it with existing `docs/BRANCH_VERSIONING_AND_INVENTORY.md` and `controls/latex/release-contract.json` without erasing historical instructions.
2. Implement a validated append-only sequence register and GitHub Action for atomic researcher-scoped reservations.
3. Add a bootstrap command and manifest generator (new source branch from HEAD, pin actual style SHA).
4. Add file-scope ownership checks and reviewer gates for global formatting changes.
5. Add reproducible optional regression matrix for **admitted/buildable** researchers; document gaps for enrolled but unbuildable ones.
6. Verify branch protection and release tag permissions; then use actual GitHub tests before declaring automation active.

**Keep it lightweight:** no duplicate tower, no 11 copies of the style, no new Drive version counters for Git source changes, no mandatory source rebuild for every unrelated commit.
