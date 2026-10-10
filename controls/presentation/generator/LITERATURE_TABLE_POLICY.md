# A9 academic presentation — source-linked literature tables (v0.1)

## Presentation design

**Default: 3 columns.** `Author (Year)` | `Key Finding` | `Relevance to This Study`. The third column contains the researcher's own explicit analytical connection to a thesis objective, not another claim attributed to the source. An optional **4-column** layout adds `Method / Limitation`, but only when method matters and has been checked against the paper. Never make four columns mandatory.

Use a structured `literature_references[]` registry and `literature_table.rows[]`, never a hardcoded list of author names or fixed paper counts. Each row cites `reference_id`, which points to a canonical BibTeX entry, exact author/year, source kind, and admitted `source_id` from a project-specific evidence map. Manuscript sections, original source locators, and relevance to thesis objectives are mandatory. No anonymous "studies show" assertions. No guessed author/year, fabricated DOI, invented findings, or imported statistics.

The Python engine expands a long matrix into several pages, at most three rows per page, preserving each entry and retaining the 4:3 PU slide size. Authors and findings remain editable native PPTX table cells. PDF uses ReportLab with a matching grid. The PDF and PPTX are generated from the same verified JSON source; they must not be edited separately. Default figures or literature not in the manuscript must NOT be introduced automatically.

## Scientific validation boundaries

1. Resolve **CURRENT manuscript source and exact Git commit** before authoring, not prior slide decks.
2. Parse the manuscript's active `.bib` keys, its relevant chapter/sections and the underlying source paper; record author/year/title/DOI/URL without inference.
3. Read the actual cited study's conclusion or specified evidence. Record `finding_locator` (page, section, figure or table) and only paraphrase what is supported. A thesis citation alone is not proof of precise source findings.
4. Link each source to the A9 evidence map; status must be `ADMITTED_CURRENT` or `APPROVED_CURRENT`, never CANDIDATE/REJECTED/SUPERSEDED/PRIVATE_ONLY.
5. `project_relevance` is an interpretation to be separately justified by `relevance_basis` (thesis objective/section). Avoid claims that a foreign study establishes local site measurements or engineering compliance.
6. Keep technical codes/standards/manufacturer manuals distinguishable from peer-reviewed studies using `source_kind`. State applicability conditionally (building system, revision, manufacturer).
7. An unverified or unavailable underlying paper must be excluded or marked for researcher review; the engine **must fail** for unknown references or missing locator/admission.
8. Machine semantic gate checks IDs, statuses, text limits and relationship fields. It **does not certify paper accuracy, interpretation validity, or supervisor approval**. A reviewer must read cited sources.
9. No internal system/checkpoint terms should appear inside the presentation; QA/provenance details belong in sidecars.
10. Render and inspect every slide for clipping/overlap, font identity and citation legibility. Do not reduce font to illegible size; split long tables.

## Suggested inheritance

`controls/presentation/generator/` owns all reusable Python rendering/validation code. `researchers/{slug}/presentation/` holds researcher-specific JSON and a private evidence map reference. Never copy author rows from Safal into Nabin or vice versa. The A9 Drive control tower remains scientific/file authority; GitHub owns source code and history. Preserve historical release IDs, snapshots, and Local/Main status independently.

## Reviewer checklist

- [ ] All rows match current manuscript and bibliography.
- [ ] Each finding checked against the original referenced source and locator.
- [ ] Relevance maps to explicit thesis scope/objective.
- [ ] Source types and code applicability correctly distinguished.
- [ ] Three-column default used; four-column justified.
- [ ] All long matrices paginated and slides visually inspected.
- [ ] PDF/PPTX text and row order identical.
- [ ] Supervisor/researcher approved the scientific interpretation.
