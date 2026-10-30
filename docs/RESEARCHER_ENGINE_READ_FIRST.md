# Researcher engine — read first

Applies to every identity enrolled in `registry/researchers.json`; shared authority
remains `controls/latex/tower.json`. No second control tower is created here.

## Resume procedure

1. Fetch live main; record its SHA. Read root and researcher AGENTS, Memory Wall,
   inheritance/versioning protocol, tower, semantic policy and owner registry rows.
2. Resolve the owner's live Drive scientific source, CURRENT and audit. Chat history
   and old placeholder branches cannot override these authorities.
3. Inspect pending PRs and existing pinned manifests. Fresh revisions inherit the
   latest approved main template; existing releases/branches retain tested pins
   until an explicit upgrade and regression QA.
4. Preview the sequence with `researcher_sequence.py --dry-run --slug SLUG --topic TOPIC`.
   Unverified baselines stay held; Saugat's floor is 028 and Nabin's observed
   release highwater is 056. Preview numbers are not reservations.
5. For authorized new work, run the reservation workflow in request mode. It opens
   a ledger-only PR. Merge through required validate, up-to-date and scope gates.
   Competing PRs for the same sequence must be replanned after the first merge.
6. Run finalize mode with the merged reservation request key: it reads canonical
   main, creates the recorded researcher branch, and pins the exact current style
   blob/version and base commit. No main write occurs. Retry with the same key.
7. Edit only owner source. Shared improvements use a separate global PR. Keep
   results and required limitations honest; put internal status matrices and audit
   narration in the same researcher's governed Google Doc.
8. Source/PDF QA, Drive hash readback and authorized CURRENT promotion remain
   separate. Governance enrollment never certifies a manuscript or upgrades a PDF.

## Evidence-first execution contract

This operational contract applies to all registered researchers and all lanes,
under the existing tower's evidence, isolation and disclosure rules.

- Start each session with the live main SHA and exact owner identity. Read the
  owner's current control, source manifest, pending PRs and scientific checkpoint.
  Historical instructions below later superseding addenda are archival context.
- Before changing a factual claim, open its exact owner source. Record the file
  ID/revision or Git SHA, page/table or sheet/range, units and calculation lineage
  in the existing private owner audit. Bibliographic existence and claim support
  both need verification; never invent references or infer a test from an image.
- Distinguish observed facts, derived calculations, interpretations and unknowns.
  A null pointer, inaccessible source, source conflict or missing approval stays
  unresolved. Hold the dependent claim/write; continue independent verified work.
  Do not create empty audit files or folders merely to satisfy a checklist.
- Never borrow another researcher's results, model assumptions, cases, citations
  or approval. Safal Thapa and Safal Dawadi are separate identities.
- Keep actual methods, supported findings, concise material limitations and
  required assistance disclosures in the manuscript. Preserve displaced internal
  status details in the same owner's existing versioned Google Doc audit first.
- Preview, source lint, compilation, exact-font page QA, science review, Drive
  byte readback and CURRENT promotion are independent states. Report a check as
  passed only after executing it on the exact candidate. No enrollment or lint
  result certifies scientific truth, building safety or university acceptance.
- Fresh controls govern new work. Existing template pins and released PDFs remain
  unchanged until an explicitly authorized migration/release passes its gates.
  No direct main writes, force pushes, guessed sequence numbers or automatic CP.

These safeguards reduce unsupported claims; automated checks cannot guarantee
factual correctness or make another chat read GitHub automatically.

## Workflow token and operational status

Dry runs need read access only. Request/finalize writes require the repository
secret `RESEARCHER_ENGINE_TOKEN` (a suitably scoped GitHub App or fine-grained token
with contents and pull-request write access). This allows ordinary PR CI events;
GitHub's default GITHUB_TOKEN-created PRs do not normally trigger PR workflows.
No credential belongs in chat or Git. Missing secret causes a visible stop.
No real researcher sequence is consumed to test this infrastructure. The live
write path remains unverified until an authorized reservation is actually run.

## Chat continuation

Repository enrollment does not modify other ChatGPT conversations. At the next
use of an older thread, paste the short instruction below once. Later sessions
should continue resolving live authorities, rather than retaining a stale version.

> Resume this researcher using live main of FabinGurung/JP_Research-and-Development.
> Read AGENTS.md, docs/RESEARCHER_ENGINE_READ_FIRST.md and the owning
> researchers/<slug>/AGENTS.md. Apply current shared controls and semantic rules;
> preserve scientific data, existing template pins and CURRENT. Report live status
> before continuing; never guess or allocate an unverified sequence.

## Rollout scope — 2026-10-30

All 11 registered identities receive entrypoints and shared-policy references.
No scientific source, PDF, Drive CURRENT, shared style or old release is changed.
`validate` includes enrollment, allocator and scope regression checks, making the
already-required check cover governance without needing another settings change.

## Ongoing QA

Required `validate` checks all-owner routing and mutation regressions, runs the
advisory semantic scan, and retains `researcher-engine-source-qa` as a workflow
artifact. Reproduce with `python scripts/latex/audit_researcher_engine.py`.
[30 October source audit](audits/RESEARCHER_ENGINE_QA_20261030.md) records the
repair and exact unresolved boundaries. A dated receipt is never live authority.

## Artifact currency is a separate check

Before calling a researcher's project up to date, inspect the actual owner LaTeX/DOCX,
compiled PDF, discussion, audit and related artifact manifests. Engine enrollment
and a passing governance scan do not migrate the artifact. Record the exact template
blob and source identity, semantic review, compile/font/visual QA, provider byte
readback and CURRENT release state separately. Reconcile candidate vs production
and Git vs packaged-source divergence before writing. Follow the existing tower's
admission/release gates; do not repair a missing baseline by inventing a sequence.

The [30 October artifact audit](audits/RESEARCHER_ARTIFACT_SYNC_20261030.md)
records executed Doc updates and discovered migration debt, without certifying all
researcher artifacts. A dated receipt never overrides a fresh provider read.

## Three-format submission contract (31 October 2026)

Read [Researcher deliverables](RESEARCHER_DELIVERABLES_READ_FIRST.md), inherited
from the existing Academic Writing tower, before creating or updating artifacts.
Rule RD-LTX-CORE-017 / RD-LTX-CHG-116 adds a separately verified native submission
Google Doc matching the admitted LaTeX/PDF revision, while keeping audit,
discussion, Colab notebook and human intake Sheet separate. Use A7 stable live
identities, numbered subject PRE/POST archives and restore-in-place history.
See the [updated general resume command](../prompts/RESUME_RESEARCHER_DELIVERABLES.md).
The contract/receipt validator is active code; actual owner conversion, native
render parity, provider execution and submission acceptance are separate gates.
