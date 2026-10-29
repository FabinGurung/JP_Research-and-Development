# R&D Memory Wall — Operating Constitution (PROPOSED v0.1)

> **Status: proposal on an unmerged Git branch, NOT an enacted control.** Date: 2026-10-30. Scope: `FabinGurung/JP_Research-and-Development`. This Memory Wall is a human/AI **navigation and principle document**, not a second LaTeX tower, a private evidence vault, or independent scientific approval.

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

**Precedence:** official original scientific/citation/academic authority for facts; existing current R&D `main` machine contracts for operations; this proposal only becomes binding once reviewed, updated where necessary, validated and merged. Old historical manifests may be stale. Never use chat history to override provider evidence.

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

**THIS DRAFT PR:** explains how these pieces interact and proposes a standard sequence + inheritance lifecycle. It does **not** alter formatting code or scientific source.

**NOT YET IMPLEMENTED:** atomic per-researcher `seqNNN` allocator, new-branch bootstrap command/action, mandatory style-pinning manifest fields for every researcher, cross-researcher production visual regression automation, CODEOWNERS/main branch protections where not provider-verified, mandatory CI path-owner enforcement.

Implement those deliberately in a separate PR after the proposal is accepted, checking actual GitHub permissions and existing workflows first. Never call them active until provider readback and CI prove they are.
