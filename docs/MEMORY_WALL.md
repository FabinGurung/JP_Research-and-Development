# R&D Memory Wall — Operating Constitution (v1.0)

> **CURRENT PROCEDURE:** Read [Researcher engine — read first](RESEARCHER_ENGINE_READ_FIRST.md) before acting. Its protected-main PR procedure and evidence-first contract supersede historical direct-main commands and implementation-status notes below. Historical records remain preserved.


> **Status: USER-APPROVED GOVERNANCE; implementation in GitHub source control.** Adopted via PR #62 on 2026-10-30. Scope: `FabinGurung/JP_Research-and-Development`. This Memory Wall is a human/AI **navigation and principle document**, not a second LaTeX tower, a private evidence vault, or independent scientific approval.

## Table of contents

1. What is authoritative?
2. The core operating principle
3. What the repository already has
4. How one researcher begins a new version
5. Shared-template improvements from any researcher
6. Sequence, tag, and artifact identities
7. Concurrency and no-collision guarantees
8. Release/rollback and scientific signoff
9. Implementation status and next gates
10. [Three-format submission bundles and working records](#three-format-submission-bundles-and-working-records)

## 1. What is authoritative?

Use **GitHub as the source/history authority** and **Google Drive as the scientific/private-binary custody authority**. University/researcher/supervisor evidence is the approval authority. A7 is a **read-only catalogue** for this module and does not own or mutate R&D source.

Read the actual machine owners; this document points to them, it never clones their rules:

- [Git/Drive authority](GIT_DRIVE_AUTHORITY_READ_FIRST.md) → [machine contract](../controls/git-drive-authority.json)
- [One LaTeX control tower](../controls/latex/tower.json) → [one shared style](../controls/latex/template/pumlsc-shared.sty)
- [All researcher inheritance entries](../registry/latex-inheritance.json), [researcher registry](../registry/researchers.json)
- [Global/local amendments](../controls/latex/change-register.json), [extension registry](../controls/latex/extension-registry.json)
- [Build and QA controls](../controls/latex/build-contract.json), [QA](../controls/latex/qa-contract.json), [release](../controls/latex/release-contract.json)
- [Branch-history principles](BRANCH_VERSIONING_AND_INVENTORY.md), [agent entrypoint](../AGENTS.md)
- [Detailed researcher/template protocol](LATEX_TEMPLATE_INHERITANCE_VERSIONING.md) (proposal attached to this Memory Wall)

**Precedence:** official original scientific/citation/academic authority for facts; existing current R&D `main` machine contracts for operations; this document is an approved policy; machine controls and successful GitHub checks govern which automated capabilities are operational. Old historical manifests may be stale. Never use chat history to override provider evidence.

## 2. Core operating principle

**ONE FORMAT, MANY OWNERS, NO SCIENTIFIC MIXING.**

Each enrolled researcher:
- Starts a unique numbered workstream **from fresh `main`**, so it sees the latest *approved* shared template.
- Works exclusively in their own research source and metadata, and uses *one* inherited template path. No shadow copies of the base style.
- Can propose a formatting improvement to the shared template **only through a separate globally reviewed change**, with reproducible before/after evidence, regression tests and a numbered `RD-LTX-CHG` entry.
- Receives a template change on **new branches automatically by using newer `main`**. Existing/frozen branches/releases **never change themselves**: refresh is an explicit rebase/merge with validation.
- Uses independent scientific admission and Drive PDF/source SHA readback before promoting a new thesis CURRENT.

**Git commits are historical truth.** Sequence numbers label individual researcher workflow versions. Template semantic versions label the shared formatting API. Do not confuse them with scientific CP checkpoints or Drive stable IDs.

## 3. What the repository already has (observed 2026-10-30)

- One canonical LaTeX tower and `pumlsc-shared.sty` v2.4.
- An inheritance registry with **11 enrolled researcher identities**. Enrollment does **not** mean all 11 have admitted active manuscript source or production PDFs.
- Researcher-only adapters under `researchers/<slug>/latex/extensions/` and a single global amendment register.
- Historical branches `researcher/<slug>/latex` that may be EMPTY/legacy placeholders. These are not automatically active manuscript source branches.
- An approved scoped Git/Drive cutover. There is no single existing named Memory Wall file in this R&D repository on the inspected `main`.

Do **not** recreate a second LaTeX tower or treat the old `branch-registry.json` placeholders as production truth. The current accepted source is the actual Git `main` tree; stable Drive CURRENT pointers are separately authoritative for binaries.

## 4. How a researcher begins a new version

See [exact procedure](LATEX_TEMPLATE_INHERITANCE_VERSIONING.md). Human-friendly instruction:

> Start a new LaTeX revision for `<researcher>`. Read their CURRENT manifest and latest main. Allocate (do not guess) their next unclaimed researcher sequence. Create a numbered branch from the latest main SHA. Pin the shared template version/source commit in the researcher revision manifest. Keep all scientific changes inside that researcher's own folder. Report PRE source SHA and outstanding evidence.

**Proposed branch namespace:** `thesis/<slug>/latex/seqNNN-<topic>`. The `thesis/` prefix avoids a real Git reference collision with existing branches named `researcher/<slug>/latex`. Do not create `researcher/<slug>/latex/seqNNN`: the legacy leaf ref blocks that nested name.

Every branch points to an entire repository commit; it is **not a folder-level private database**. GitHub permissions and PR guards must prohibit cross-researcher files without explicit approval.

## 5. Shared improvements are reviewed once and inherited safely

A Saugat, Nabin or Safal finding can be:

1. **Research-specific content:** in the owning researcher's source branch only; it cannot become a global format rule.
2. **Researcher-specific format need:** a small registered extension; keep central base template unchanged.
3. **Genuinely global format defect:** file a `GLOBAL_CANDIDATE` amendment, prove with before/after pages, review against original university format evidence, patch the **single** shared template, run shared validators and available active researcher regressions, version the template and merge a separate global PR.

A successful *one-researcher* render does not certify all other researchers. Researcher releases pin the tested template commit; new branches take the new `main` version. Existing active branches choose explicitly whether to refresh and re-test. For potentially breaking major format changes, warn/require manual migration.

## 6. Never conflate these version identities

| Identity | Example | Meaning |
|---|---|---|
| Researcher | `RSH-002 / saugat-paneru` | Stable owner key |
| Scientific checkpoint | `CP114` | Approved study-data/content lineage |
| Researcher LaTeX sequence | `seqNNN` | Unique sequential **researcher** revision; allocate using a per-researcher register before creating branch |
| Shared-template version | `v2.4.0` | Single LaTeX format library revision; increment only on global template change |
| Global change ID | `RD-LTX-CHG-114` | Central change register, NOT the thesis sequence |
| Commit SHA / tag | exact Git SHA / approved annotated release | Immutable content identity and rollback |
| Drive file ID + SHA256 | stable `CURRENT_CHECKPOINT` and PDF source IDs | Deliverable/evidence custody |

Every released PDF must record: researcher ID, scientific CP, manuscript sequence/version, shared-template exact source SHA/version, owning source Git SHA, private original asset manifest, compiler/font specification, PDF Drive ID/hash, and approval/QA status.

## 7. Concurrency must be explicit

- Different researchers may work in parallel off `main`. PR path scopes isolate Saugat scientific files from Nabin scientific files.
- Shared files (`controls/latex/**`, `registry/**`, `.github/**`, website code) are **explicit shared ownership**, not a researcher default. Review changes independently.
- Every new PR rechecks latest `main` before merge. When `main` advances, bring new changes by non-force rebase/merge and re-run tests. Never assume old PRE HEAD remains main.
- Proposal for robust numbered allocation: append-only per-researcher sequence register on `main`, created with a serialized/optimistic-lock reservation transaction, unique `researcher_id + lane + seq`, GitHub issue/PR linkage. If two writers race, reject/reallocate rather than silently reuse a number. **This allocator does not yet exist; do not claim it does.**
- Protect main with required checks, non-force merges, and (where supported) path owners for shared format files.

## 8. Release and rollback

`fresh main → reserved seq branch → source edits → QA/science evidence → PR → accepted source in main → compiled candidate → Drive provider SHA readback → updated production manifest + stable CURRENT (only with authorization) → annotated Git release tag (major milestones)`.

Do not equate code CI, an unsigned print-proof certificate, or a successful PDF render with university format certification. Keep old Git tags, scientific originals, Drive PDF/ZIP and checkpoint PRE snapshots intact. Do not auto-increment historical A9 Drive Local/Main counters for routine Git source changes.

## Read-first protocol for future ChatGPT/researcher sessions

A new session must resolve authorities in this order: (1) current GitHub `main` SHA; (2) this Memory Wall; (3) actual current domain machine tower/control; (4) the owning researcher's version/source and style manifest; (5) current Drive scientific source and PDF/checkpoint; (6) pending PR/CI/debt. **Do not use previous chat narrative to overwrite current source evidence.** A Memory Wall is an address-and-operating-principle navigator, not a substitute for audit trails, old chat archives, Git source history or Google Drive original research.

## Known reconciliation debt to clear before making this binding

These are **observed discrepancies**, not reasons to rewrite history:
- `controls/latex/README.md` still has a `2.3.0` heading although current `controls/latex/tower.json` records `2.4.0`. Fix the stale heading after agreeing the single release/version policy.
- Historical `registry/branch-registry.json` marks researcher's `researcher/<slug>/latex` placeholders as empty. Saugat/Nabin instead have active source on `main` and more recent task branches; do not mistakenly build from placeholder refs.
- `controls/latex/release-contract.json` retains older A9 Local/Main ACK states and fields; current scoped `controls/git-drive-authority.json` supersedes that routine Git-version work. Review/update the subordinate contract without asserting older unacknowledged history was completed.
- Existing 11 inheritance entries are metadata enrollment, not eleven fully source-admitted/buildable theses.
- No verified atomic per-researcher sequence allocator or global template-change owner gate exists yet. This proposal defines the intended contract, not implemented automation.

Any correction should receive its own scoped PR, preserving historical records and validating all current source-gates.

## 9. Implementation status

**ALREADY REAL:** single template path; 11 registered identities; extensions; central change register; Git PRE/POST; CI source checks; Drive release hashes on governed researcher releases.

**PR #62 MERGED:** read-first principles adopted; no scientific source or shared formatting code changed.

**IMPLEMENTATION PR:** [sequence allocator and path-scope CI](https://github.com/FabinGurung/JP_Research-and-Development/pulls) provide dry-run-first per-researcher reservation and template-pinning for newly created numbered branches. A successful live reservation and protected-main permissions are NOT yet provider-verified, and full cross-researcher production PDF regression remains evidence-gated. Historical branches are unchanged; no current scientific source or PDF is modified.

Implement those deliberately in a separate PR after the proposal is accepted, checking actual GitHub permissions and existing workflows first. Never call them active until provider readback and CI prove they are.

## Implementation entry points (approved 2026-10-30)

- Number register: [researcher-latex-sequences.json](../registry/researcher-latex-sequences.json). Verified historical highwater Saugat 028 and Nabin 054; the other nine require prior sequence reconciliation.
- CLI: [researcher_sequence.py](../scripts/latex/researcher_sequence.py) (`--check`, `--self-test`, `--dry-run`, `--reserve`). The write path uses GitHub Contents API compare-and-swap, creates a branch and pinned version manifest, and optionally opens a draft PR.
- GitHub Actions: [Reserve numbered researcher LaTeX branch](../.github/workflows/latex-reserve-researcher-sequence.yml) — `workflow_dispatch`, **dry_run defaults true**. Do not bypass authorization or manual project selection.
- [Researcher ownership and shared-template inheritance CI](../.github/workflows/latex-researcher-inheritance.yml), [scope verifier](../scripts/latex/check_researcher_change_scope.py). Source/format gates are not final PDF or university scientific certification.
- Main/branch protection and `GITHUB_TOKEN` write entitlement could not be inspected with the current GitHub integration (HTTP 403 on branch protection read); do not claim protected-main writes or actual reservation are live-tested until successfully tested.


## 10. Live implementation reconciliation — 2026-10-30 (non-destructive addendum)

This later readback **supersedes only the historical implementation-status sentences above**, not the approved constitutional principles. GitHub main immediately before the current infrastructure repair branch was `ae338cd3e7efe121fcf56246d269f7f5d52211dc`, including the separately merged semantic-only PR #67 (shared policy v1.1; `RD-LTX-SEM-011..013`, `RD-LTX-CORE-016`, `RD-LTX-CHG-115`). The scientific Saugat M4 CURRENT Drive pointer and manuscript were unchanged.

**Observed implementation:** PR #63 was merged; workflow no-write smoke `40989763289` completed successfully. `scripts/latex/researcher_sequence.py` and the workflow provide source-level atomic CAS and branch/manifest creation *code*, but no real reservation/run has been performed and write-capable `GITHUB_TOKEN` behavior is not verified. The repo `main` branch was reported by the GitHub Branch API as `protected=false`, and branch protection detail returned integration HTTP 403. There were no active rulesets returned. This is **not a protected-main environment**. The connected GitHub account permits push but not admin, so the responsible repo administrator must configure required checks, reviewer/force-push restrictions and branch protection.

**Sequence conservation:** Nabin's earlier register baseline 054 is historically correct for the allocator cutover, but the current Git source already contains `SEQ055_ACADEMIC_ABSTRACT_AND_FULL_RESULT_FIGURES_20261030.md` and `SEQ056_TABLE46_BLOCKS_1_AND_4_20261030.md`. These are **out-of-band releases**, not allocator reservations and not evidence of scientific acceptance. The safety repair PR records both in `observed_out_of_band_versions`, causing the no-write Nabin planning output to advance to 057 **without reserving 057**. Existing out-of-band release paths and any new unregistered remote release visible on the latest main Git tree must fail closed before reserve writes. Saugat remains historical floor 028; other nine baselines are **HOLD** until each individual's actual version lane is reconciled with provider records (a Drive Local sequence is not automatically a LaTeX version sequence).

**Source isolation:** Legacy explicitly researcher-named Saugat and Nabin PR branches must never edit the other's LaTeX, even if just one researcher's files are in the diff; no PR may combine researcher-specific LaTeX files with shared LaTeX controls. Ownership checks must run on stacked PRs against their true PR base, not assume every PR targets `main`. Generalized shared prose rules are a separate global PR, and the shared `.sty` remains unchanged.

**Regression boundaries:** Unit tests and source CI demonstrate reference checking and simulated collision/ownership failures without allocating any real number. One single inherited template blob exists at `controls/latex/template/pumlsc-shared.sty`, currently v2.4.0; template SHA pinning is covered by source policy but not a live release of every researcher. Full university-font PDF regression, all 144 rules, actual write-backed reservation, and all nine unknown baselines are separate pending gates. Do not mislabel CI as code compliance or institution approval.

**A9 closeout:** This Git source-only governance repair does not update legacy A9 Local/Main Drive sequence/ACK cursors and must not fabricate one. Preserve the authoritative scientific Drive files, stable file IDs and CURRENT pointers. Any corresponding Drive audit receipt records the actual PR, check conclusions and pending administrator work; it does not become a second version-control tower.


## Protected-main and all-researcher rollout — 2026-10-30

This addendum supersedes earlier direct-main reservation instructions and old
protection observations. Branch API readback confirms main protected with required
`validate` for everyone. See [current engine procedure](RESEARCHER_ENGINE_READ_FIRST.md).
All 11 owner entrypoints inherit the live tower and semantic policy, without
changing frozen pins, scientific source, CURRENT or unverified sequence histories.
Reservations now use a ledger-only PR, latest-base validation, then post-merge
bootstrap. Actual write execution remains unverified; default is no-write.

## Three-format submission bundles and working records

User-authorized 31 October 2026: [RD-LTX-CORE-017 deliverable contract](../controls/academic-writing/research-deliverables.json),
owned by the existing Academic Writing tower, links the same admitted scientific
revision to complete LaTeX, compiled PDF and a native submission Google Doc.
The Doc needs independent exact content/format/pagination comparison with the PDF;
audit/discussion Docs, Colab analysis notebook and human intake Sheet remain
separate. Presentation source remains JSON/Python under its existing tower.
Follow the [execution and versioning guide](RESEARCHER_DELIVERABLES_READ_FIRST.md)
and [researcher resume command](../prompts/RESUME_RESEARCHER_DELIVERABLES.md).
This inherits A7's permanent live-ID, enumerated PRE/POST, append-only history and
restore-in-place policy without editing A7 or certifying existing artifacts.
