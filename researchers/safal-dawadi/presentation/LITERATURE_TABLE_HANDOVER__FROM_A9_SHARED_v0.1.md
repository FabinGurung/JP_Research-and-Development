# HANDOVER — Safal Dawadi presentation literature review (after A9 shared implementation)

**Scope**: update only the literature/technical-basis section of the existing Safal presentation. Never rewrite or alter the v1.12 thesis PDF/source, old v0.7 PDF/PPTX, or previous A9 release records in place. Create the next enumerated presentation version in a separate reviewer branch and Drive folder.

## Resolve and inherit current controls

1. GitHub repository: `FabinGurung/JP_Research-and-Development`; read `controls/presentation/README.md`, `controls/presentation/tower.json`, `controls/presentation/generator/LITERATURE_TABLE_POLICY.md`, `a9_literature_table.py`, `literature_table.template.json`, `presentation_schema.json`, `a9_semantic_checker.py`, `a9_presentation_validator.py`, `a9_presentation_generator.py`, `build.py`, and CI workflow. Read from the exact validated main commit/tag (do not assume chat summary current).
2. Safal workspace: `researchers/safal-dawadi/presentation/v0.7/` (branch `safal/presentation/v0.7-building-only-review-20261010`, draft PR #13) and current v1.12 manuscript branch `safal/v1.12-building-only-cover-spacing-20261010`. Recheck for any newer release before editing.
3. Safal v0.7 Drive review folder: `1BErK6tU0cG04HSNvjf9KVthTwgAk73Ug`. Approved shared control v2.2 ID: `1i2YO58HJ1WVsYnBDP0a0ZJg-29VOPccPnWiWit08ofM`. Preserve Local Seq18 and Main cursor5 HOLD until an actual ack is provider-read back.

## Build the literature table from actual research

- Read v1.12 Chapter 2 and its active bibliography in the source ZIP and Git. Include original literature actually cited in the research, not random internet studies or a hardcoded list from the old slide.
- For each proposed source, verify the BibTeX citation, author/year/title, full source text or accessible authoritative abstract, and exact section/page supporting a concise **Key Finding**. If original publication cannot be examined, hold that row for review rather than guessing.
- Map **Relevance to This Study** to the specific Safal research objective/section and mark `relevance_type`. Distinguish literature evidence from local observational evidence; never treat published international estimates as Pokhara project measurements.
- Treat technical building standards, manufacturer manuals and guides differently from peer-reviewed research. Only retain sources actually applicable to waterproofing and masonry/plaster under the building-only scope; preserve actual code applicability caveats.
- Use `literature_table` slide type with 3 columns by default. For method-heavy rows, optionally use 4. Put at most three concise source rows per physical slide (the engine auto-paginates). Keep a separate selected full references slide only if required by institutional defense guidelines.
- Populate `literature_references[]` and source-linked rows using the standard template. The private evidence map must contain admitted source IDs and the Git commit/manuscript manifest. Do not manufacture approvals or fake `admission_status` values.
- Run the shared validator, semantic checker, render PDF/PPTX, visual QA on all slides, exact Times New Roman, official PU logo, title metadata, SHA256 manifest, PRE/archive/POST and provider readback. Record both old and new identifiers and parent-child links. No scientific-final status without supervisor approval.

**Stop conditions**: any unverified author finding; missing original-source locator; source not admitted; unsupported local data/claims; slide overflow; missing source documentation; absent human scientific review. Use HOLD, not PASS.

## Design target

| Author (Year) | Key Finding | Relevance to This Study |
|---|---|---|
| Verified author and publication year | One short, supported finding from the original publication | Specific use for the thesis objective, method, interpretation or research gap |

This is **handover only**. No modification to Safal's current PDF/PPTX is authorized by this phase.
