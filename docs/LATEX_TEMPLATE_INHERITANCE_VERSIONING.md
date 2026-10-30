# LaTeX inheritance and independent researcher sequencing — approved v1.0

> **CURRENT PROCEDURE:** Read [Researcher engine — read first](RESEARCHER_ENGINE_READ_FIRST.md) before acting. Its protected-main PR procedure and evidence-first contract supersede historical direct-main commands and implementation-status notes below. Historical records remain preserved.


This is the detailed procedure linked by [R&D Memory Wall](MEMORY_WALL.md). A dry-run-first allocator and a source ownership gate have been implemented in an implementation PR, with live Action/permissions verification required before claiming fully operational reservation. Reuse existing [single LaTeX tower](../controls/latex/tower.json), [inheritance registry](../registry/latex-inheritance.json) and [change register](../controls/latex/change-register.json), instead of creating an alternate control.

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

## Version-sequence reservation (source implementation merged; live write authorization unverified)

The implementation uses an append-only per-researcher register, `registry/researcher-latex-sequences.json` with explicit schema, entries and unique keys `(researcher_id, lane, sequence_number)`.

A reservation is an **atomic, serialized operation against latest main**:

1. Read current accepted and reserved sequence numbers; do not reuse or silently renumber historical LATEX_SEQ and M4 checkpoint labels.
2. Determine next genuinely free number in that researcher's own namespace. A visible GitHub issue/PR or task UUID owns the reservation; log parent Git SHA and original source/Drive CURRENT.
3. GitHub Actions uses a shared reservation concurrency group and the allocator additionally compare-and-swaps the register's current blob SHA on `main`; if changed it re-reads and retries. This avoids relying solely on GitHub queue ordering. No force push.
4. Append reservation with status `RESERVED` and link to exact work branch. Abandoned reservations become `ABANDONED` with an explanation, never reused. No fictitious commits.
5. On accepted PR, set `MERGED` with actual Git POST SHA. On signed-off Drive deliverables, record `RELEASED` with Drive IDs, SHA and optional approved Git tag.
6. Gate source PRs against registered scope, unallocated or duplicate seq, expected template SHA and unrelated researcher edits.

The reservation source and no-write workflow have been implemented by PR #63 and a verified dry-run smoke, but the write-capable reservation path is **not yet exercised**. Do not assert a new reservation or permission from code alone. A new branch may be allocated only through the governed transaction after main provider-state review. Nabin's existing SEQ055 and SEQ056 release records were created outside this allocator; the repair register must treat them as already used, while preserving the originally verified 054 cutover floor. The next planned Nabin value is 057 **only as a dry-run suggestion**; it is not a reserved number.

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

### Concrete use (implementation)

1. GitHub **Actions → Reserve numbered researcher LaTeX branch → Run workflow**, choosing `main`, the registered `researcher_slug`, and a short topic.
2. Keep **dry_run=true** to check the next possible number without consuming it. For Saugat 028 and Nabin 054 the verified historical anchors yield 029/055 *only if no newer reservation or branch exists at execution time*.
3. For authorized work set **dry_run=false**; the Action atomically appends a reservation using file-SHA compare-and-swap, creates `thesis/<slug>/latex/seqNNN-topic`, pins the live `pumlsc-shared.sty` blob SHA and version in `researchers/<slug>/latex/versions/seqNNN.json`, and optionally opens a draft PR.
4. **No automatic scientific approval:** researcher edits and scientific approval still occur in their own branch and controlled Drive records. Merge requires scope/QA gates and research-owner evidence.
5. Unknown historical sequence baseline = HOLD. Existing older `researcher/<slug>/latex` branch remains; no history rewritten.
6. For a global formatting change, create a dedicated `template/latex/vX.Y.Z` branch, amend the global change register with `GLOBAL_CANDIDATE`, bump the tower version, run inheritance and available researcher regression. Full Times New Roman renders for other researchers are still separate QA gates.

**Permission boundary:** Branch protection could not be inspected by the connector. If the manual GitHub Action cannot write the sequence register to `main`, it must stop with a visible error, not bypass protection or reuse a number. Before enabling production reservations, an administrator should verify the appropriate limited repository Actions/token permissions and require CI checks.

## Source-only verification additions — 2026-10-30

- [GitHub live no-write smoke](https://github.com/FabinGurung/JP_Research-and-Development/actions/runs/40989763289): verified successful, no branch or number allocated.
- GitHub branch detail has `protected=false`; protection detail read returns HTTP 403 to this connector and no repository rulesets were returned. Admin-owned security change remains outstanding.
- `registry/researcher-latex-sequences.json` now proposes `observed_out_of_band_versions` for Nabin 55/56 (real Git release records, **not fabricated reservations**); `--self-test` checks duplicate and remote-main future-release collision handling without write.
- Source owner checks include explicitly named legacy branch owner mismatch and mixed researcher/shared-control changes; `.github/workflows/latex-researcher-inheritance.yml` checks stacked PRs relative to their actual base ref.
- Bootstrap proof without allocation: the source-gate's mock manifest checks style SHA pinning, branch slug and sequence, and centralized path; the actual Git shared style blob on the infrastructure branch must remain the same as the pinned v2.4.0 main. Real branch creation/manifest publication awaits the write test and administrator protection.
- Nine unresolved researchers remain held. Their A9 Local ledger numbering and thesis LaTeX source sequence numbers must not be conflated or inferred from filenames alone. Full cross-researcher scientific or PDF regression is not claimed.


## Protected-main and all-researcher rollout — 2026-10-30

This addendum supersedes earlier direct-main reservation instructions and old
protection observations. Branch API readback confirms main protected with required
`validate` for everyone. See [current engine procedure](RESEARCHER_ENGINE_READ_FIRST.md).
All 11 owner entrypoints inherit the live tower and semantic policy, without
changing frozen pins, scientific source, CURRENT or unverified sequence histories.
Reservations now use a ledger-only PR, latest-base validation, then post-merge
bootstrap. Actual write execution remains unverified; default is no-write.
