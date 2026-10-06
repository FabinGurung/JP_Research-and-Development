# ADR 001 — Separate research, identity, governance and evidence

Status: implementation foundation; dedicated A9 deployment pending.

| Layer | Responsibility | Canonical contents | Excluded |
|---|---|---|---|
| A7 registry | Identity, aliases, authority assignments and routing | Public-safe JSON/JSONL relationships | Detailed A9 event histories |
| A9 governance | Sequence state, PRE/POST, receipts, debt and compact resume | Small machine-readable events and pointers | Scientific payload copies |
| R&D hub | Understandable public research directory and approved presentation | Project IDs, short names, public summaries and routes | Private Drive links, unpublished results and every-version audit logs |
| Google Drive | Scientific evidence and working artifacts | Sources, exports, figures, spreadsheets, LaTeX ZIPs and PDFs | Replacement by a GitHub projection |
| Specialist repositories | Executable products and experiments | Engine code and product-specific tests | Becoming the thesis evidence authority by accident |

The public R&D repository carries a deployable A9 **bootstrap package**, not an active second A9 ledger. Its CURRENT explicitly says NOT_PROVISIONED. Copy this package into the proposed dedicated repository only after its provider identity and privacy policy are verified. Live/private records must never be introduced into this public staging area.

Public directory entries are user-requested metadata. They make no claim about scientific completion, dataset quality or live thesis state. Saugat Discussion intake, LaTeX admission, supervisor commands and Drive reconciliation are deferred to a separate chat.

## Stable identity and names

Keep permanent PROJ IDs when titles change. Human labels use three to five meaningful words. Machine slugs are unique; renaming requires an alias/redirect and cross-link update. Existing /aec, /hydropower and all earlier demonstration routes remain available.

## Version and release strategy

Preserve the original provider head with a PRE snapshot branch. Use one feature branch per bounded purpose; validate and read back before promotion. A commit records a small change. An annotated tag/release records a meaningful milestone. Never force-push, overwrite a release or silently move a tag. Store a release receipt referencing the content commit; a later receipt commit avoids circular self-SHA claims.

## Migration

1. Provision A9 with a verified provider ID; select private visibility before storing restricted pointers.
2. Run its schema, invariant and privacy validation on the empty foundation.
3. Select one bounded lane, read its actual live CURRENT and latest closed event, and inventory its real debt.
4. Import pointers and receipt evidence only; mark unknown hashes/readbacks as unknown.
5. Read back GitHub and Drive, add the reverse reference in the owning Drive register under PRE/POST, then acknowledge.
6. Add the verified A7 relationship and repeat only after the pilot passes.

No bulk migration is authorized by this foundation. No existing Drive artifact has been mutated.

## Rollback

Revert the bounded Git commit through a new commit; preserve PRE branches, events and releases. Roll back a CURRENT pointer through a superseding event that names the previous target and reason. Drive scientific versions retain their existing snapshot/archive procedure. Unknown or mismatched provider state blocks promotion.

## Privacy and large binaries

Do not commit credentials, unpublished datasets, client records, proprietary fonts, manuscript PDFs or mirrored large artifacts. Record a Drive pointer, SHA-256, byte count and disclosure policy after actual verification. Public projections must omit restricted metadata and private provider identifiers. A private governance repository still requires controlled access and safe public projections.

## Resume protocol

One chat owns one lane and one bounded purpose. Read CURRENT, latest closed event, applicable policy and only the relevant delta. Carry authorities, active debt, exact next boundary and do-not-replay entries in a handover under 3,000 tokens. Close before context pressure becomes material; no interface token meter or percentage is assumed. Provider readback is mandatory before claiming completion.
