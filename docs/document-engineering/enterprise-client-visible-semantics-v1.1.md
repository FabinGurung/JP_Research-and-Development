# A9 Enterprise Client-Visible Document Semantics — v1.1

## Binding rule (approved 2026-10-19)

For **every newly authored Enterprise LaTeX project and every client-facing PDF**: show only human-readable legal, commercial, engineering or employment content. Do **not** print:

- internal lifecycle labels such as `DRAFT`, `SAMPLE`, `FICTIONAL`, `PROTOTYPE`, `NOT FOR SIGNATURE`, `QA` or `INTERNAL USE ONLY`;
- numbered project folder slugs such as `07_Example_Client`, machine keys such as `PRJ-000007`, `ORG-000001`, or snake_case identifiers such as `project_identifier`;
- AI/computer implementation labels such as ChatGPT, LLM, JSON, SQL, GitHub, script or database workflow nomenclature.

Client copies may instead say **Radha Roka Residence**, **Construction Works Agreement**, **Agreement Date**, **Contract Price**, or a genuine business invoice/reference number. Do not invent or silently rename actual persons or business/legal entities. If an input's only available name is an internal key, HOLD for the authoritative human-facing project name.

This is a **visible-output** rule, not destruction of lineage. All internal IDs, revision tags, statuses, Git SHA hashes, real QA records and original Overleaf sources stay in structured metadata, private folder/file names, comments and audit logs; do not expose them in visible documents.

## Hard enforcement

Authority: `controls/document-engineering/client-facing-language.policy.json` (v1.1).
Validator: `scripts/document_engineering/check_client_facing_language.py`.
Engine: `scripts/document_engineering/engine_v3.py`.

The active v3 engine now:
1. resolves exactly one approved canonical template for each named type,
2. verifies all required structured inputs,
3. projects the **immutable** v3 template into a client-clean LaTeX instance, hiding machine metadata, generic internal sample/status banners and styling notices without rewriting the released canonical source,
4. rejects visible client field content containing internal IDs, statuses or implementation terminology,
5. checks generated final .tex visible source,
6. compiles the PDF with shell escape disabled and checks the extracted final PDF text,
7. records the internal state and engine provenance separately in `.qa.json`.

Use this same final output gate for **any private-instance** or custom template compiler, even if it does not use the v3 engine:
```sh
python3 scripts/document_engineering/check_client_facing_language.py --self-test
python3 scripts/document_engineering/check_client_facing_language.py --tex /private/project/contract.tex
python3 scripts/document_engineering/check_client_facing_language.py --pdf /private/project/contract.pdf
```
A passing text lint does **not** approve the actual contract: source authority, code and drawing checks, numerical QA, legal/technical review, signatures and provider read-back retain their separate release gates.

### Historical and existing documents
Legacy v1/v2 files, frozen canonical v3.0.0 Git blob sources and v0.6/v0.7 Radha Roka contract PDFs **remain immutable historical evidence**. They may still show old review labels; they are **not** retroactively called compliant. A future Radha Roka revision must be compiled again and pass this rule before being considered client-ready. No edits to existing private client contract clauses are implicit in this semantic-policy change.

### Scope boundary
This controls **Enterprise Documents**. It does not change Academic Writing or other GitHub Pages website modules. The policy may change future business PDF wording but not mathematical or business terms.
