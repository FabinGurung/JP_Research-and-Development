# A9 AI-first research & enterprise family interface (v0.1)

**Two separate families, one human-facing entry.** The public website is a view over versioned machine controls, not a replacement for the private source files.

## Canonical family authorities
- `controls/family-router.v0.1.json` routes each work request.
- ENTERPRISE: `controls/document-engineering/tower.json`, typed schema under `controls/document-engineering/types/`, and 14-ID registry.
- ACADEMIC: `controls/academic-writing/tower.json` referencing the *existing*, separate LaTeX, presentation, discussion and researcher website controls.
- The academic LaTeX tower and presentation tower are **unchanged**. Neither references enterprise contracts as a source of academic truth.
- The homepage shows only Home, Enterprise Documents and Academic Writing. Academic subpages retain their original stable URLs and are catalogued under Academic Writing.

## Template normalization — no destructive writes
Review `registry/enterprise-template-normalization-audit.v0.1.json` before a cleanup. 14 canonical draft types, 3 superseded prototype sources, 1 short-form contract variant on main and 1 letterhead variant on the Radha Roka development branch.
A document type is a semantic role; a layout variant is **not** a new type. No source file has been deleted, migrated, or silently rewritten for deduplication. Historical Bishal source ZIP remains private and immutable.

## Agent-first execution protocol
`controls/ai-execution-contract.v0.1.json`, `schemas/ai-job-request.v0.1.schema.json` and `scripts/ai_runtime/validate_job.py` define the boundary between any AI orchestrator and deterministic operations.
The user gives instructions in natural language; the model resolves authorities, prepares typed input, calls authorized deterministic tools, and presents a validation-backed output. A computer is still needed **behind the AI**—compilers, database, GitHub Actions and private Drive access; users need not operate them manually when the authorized integration exists.

### Replayability
Identical canonical request JSON and pinned source bytes produce an identical request fingerprint. That does **not** mean an identical natural-language prompt always yields correct/identical output. Changed Drive records, model interpretations, dates, dependencies, PDF timestamps, unstable fonts or runtime versions can change output. We must capture these dependencies and HOLD rather than fabricate consistency.

For a serious "100/100" target, demand zero silently accepted unsupported facts, strict machine assertions, explicit conflicts, immutable source pointers, independent review gates and error disclosure. Do not promise literal zero hallucinations or that legal/scientific approval can be automated from prose alone.

### Supported now
- Public-safe family routing controls and template audit.
- Site navigation and two family dashboards.
- Fourteen typed draft templates and arithmetic/source tests.
- Canonical request structural validator and deterministic input fingerprint.

### Not yet built or certified
- Direct AI-to-private-job-runner execution bridge, universal identity/permission scopes, fully pinned TeX/PDF bytewise reproducibility.
- Individual template legal and scientific certification.
- Deleting/merging superseded source templates; requires user QA.
- Automatically signed agreements, regulatory approval, scientific proof or a 100% correctness guarantee.
