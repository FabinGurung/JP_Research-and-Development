# Project contract lane — PRJ-000029 / REB-002

This is an **explicitly authorized project-specific Git branch**, not a new shared LaTeX template and not a separate copy of every project. A Git branch tracks an entire repository snapshot; the allowlist limits this lane's intentional changed paths.

## Source architecture
- **Single approved shared template:** [client-contract.tex](../../../v3/client-contract.tex)
- **Shared compiler:** `scripts/document_engineering/compile_v3_private_client_instance.py` in this repository.
- **Per-client edited LaTeX body, logo, full legal/financial terms, source PDF and rendered contract:** private **Google Drive** in that client's governed agreements folder. Neither full client body nor the PDF is safe to commit to this public repository.
- **Public-safe semantic schema:** `schemas/enterprise/client-contract-instance.schema.json`.
- **Client status:** Draft, not signed, not engineer-approved.

## Version sequence
Use existing commit SHA as PRE and this project's registered branch HEAD as POST. A private source ZIP containing the exact `.tex` and its style/logo dependencies plus compiled PDF is uploaded to Drive under the approved project folder. Log source SHA-256, generated PDF SHA-256 and Drive provider IDs in the private source package. Never infer private-contract approval or publication from a passing workflow.

## Project-specific required validations
Milestones must use an auditable amount sum; displayed percentages can round to 99.99% while exact NPR instalments control 100%. Original architectural/structural sources can be `AVAILABLE_AS_RECEIVED_NOT_SIGNED`: they are not "missing" and not automatically approved. Plumbing/sanitary/electrical and compound/railings may be subject to Contractor–Client mutual agreement. Unpriced VO-01 rear decorative butta and VO-02 MS→SS railings must remain `null` priced until a signed VO, and SS covers all included railing locations. Client/private amount values are never checked into this public repo.

## Publication
Communications & Web may publish a **public-safe, authorization-aware pointer** only after the current project-publication settings explicitly allow it. No contract PDF, full LaTeX instance or private numeric schedule goes onto public GitHub Pages.
