# A9 Enterprise Document Engineering v2 — READ FIRST

**Status:** A9-controlled DRAFT TEMPLATE INFRASTRUCTURE. This is not a legal certification, an accepted contract, or an authorization to issue documents.

## 1. One shared enterprise tower
- `controls/document-engineering/tower.json` — canonical enterprise control.
- `controls/document-engineering/semantic-handrails.v2.json` — 14 document-family factual checks, forbidden assumptions and human review obligations.
- `controls/document-engineering/types/<document-id>.json` — required facts for every type and eight HOLD gates.
- `templates/enterprise/v2/enterprise-shared.sty` — shared LaTeX presentation.
- `templates/enterprise/v2/<document-id>.tex` — 14 typed draft sources.
- `scripts/document_engineering/engine_v2.py` — 14-template field validator/draft renderer.
- `scripts/document_engineering/validation_v2.py` — Decimal financial, payroll and inventory arithmetic.
- `registry/enterprise-document-types.v2.json` — navigable type registry.
- `enterprise-documents/control-tower/` — public-safe visual index.
- Older three templates in `templates/enterprise/` are historical prototypes; they are not the v2 sources.
- Academic thesis control `controls/latex/tower.json` and presentation control `controls/presentation.control.json` remain separately governed.

## 2. Original Overleaf archive and source control
Original, 102 files: private Drive ID `1wW-_B6bvETGFN_L7XMWcBZlUYBMTqzFP`.
All 102 private files are stored by family in A9 `02_EXTRACTED_PRIVATE_SOURCE` and checked by name/size.
A9 original-source QA register: `15O8uHISWtMnvGJPW72-kO-vGdHLVJPqU`.
- 73 TeX, 24 images, 4 PDF and 1 extensionless original.
- 46 original .tex sources reference inputs/assets; not all dependency closure is verified.
- Revised audit v0.3: 46 source files reference external dependencies; no high-risk primitive matched the corrected simple pattern. Human review remains necessary.
- Original archive and per-item source files are NOT published in this public repo.
- Per-file remote hash readback and legal/type-fidelity certifications remain pending.

## 3. Eight independent gates
G01 source and company/project authority; G02 semantic and clause provenance;
G03 typed values and applicable arithmetic; G04 document completeness;
G05 actual LaTeX/PDF compile; G06 all-page visual review;
G07 human legal, commercial, HR or technical approval; G08 approved output stored in private Drive with provider readback and correct Local/Main registration.

**Technical source tests do not automatically mark G01-G08 as PASS.**
The renderer always labels its output DRAFT_NOT_SIGNABLE. External review/release is a distinct governed transaction, not an optional formatting step.

## 4. Current QA
- `python3 scripts/document_engineering/engine_v2.py --self-test` tests all fourteen types.
- `python3 scripts/document_engineering/engine_v2.py --demo-all --out /tmp/a9-v2` builds fictional LaTeX sources and QA traces.
- GitHub workflow `enterprise-document-v2.yml` checks the typed model, required fields and arithmetic rejection.
- GitHub workflow `enterprise-document-pdf-smoke.yml` separately attempts fictional PDF builds of all fourteen types, with private inputs explicitly prohibited.
- Date ranges are checked; estimates, quotations, purchases, inventory and payroll carry arithmetic checking when structured quantitative inputs are provided. Missing structured data produces an explicit HOLD rather than invented quantities.
- This is source/system validation, NOT an attested legal or engineering compliance suite.

## 5. Client contract precedent, Radha Roka
Bishal main client contract is a private reference only; the copied project rates, parties, scope, address, financial milestones, and legal specifics must not transfer into Radha by default.
Private Bishal-to-Radha clause mapping: Drive ID `18XgTt7CAuOpEatWI-1jJosjuR63uey8z` (eight sections, 32 numbered clauses mapped).
Radha measurements: Drive document `107L3koohblEPgscjK5MQUARmPRcQglz2BOwZ7AT-1Wk`.
Old Radha PDF: Drive ID `1dhDynb_WHD0nag2JBldD-JEAMX66wft8`, explicitly FAILED WORKING CANDIDATE, preserved as rollback evidence.
No new signable Radha contract is authorized until both parties, liability, measured quantities, contractor/client works division, tax/rates and milestones are verified and legally reviewed.

## 6. Authority and rollback
Git source commits/PRs are rollback history, but the live A9 Google Drive private records own legal facts, raw originals and issued outputs.
Do not delete or mutate legacy source documents. Do not invent approvals or certify historical templates from compilation alone.
Current private checkpoint: `13rdwOeH19vE8UPa-KEoTJaa28U1LDkYM`.
A9 Main Library registration remains a separate governed transaction, not silently claimed here.
