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
   Nine unknown baselines stay held; Saugat's floor is 028 and Nabin's observed
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
