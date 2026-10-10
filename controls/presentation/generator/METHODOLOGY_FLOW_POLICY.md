# A9 shared methodology-flow control amendment — v0.1

**Scope:** One shared component `methodology_flow`, researcher-neutral. The workflow/renderer is owned by `controls/presentation/generator/`; per-researcher scientific stages and manuscript evidence stay under `researchers/{slug}/presentation/`, preferably in a candidate file until the owning researcher reviews it. This amendment does not update or approve any manuscript, prior PPTX/PDF, or supervisor judgment.

## Default visual contract

- Primary layout: `horizontal_linear`, left-to-right, for PU 4:3 **landscape** academic slide. Do **not** silently switch the entire deck to 16:9 to accommodate a flowchart.
- Three to six nodes per slide (prefer five or six). Seven or more nodes automatically **paginate**; never shrink below readable font sizes or snakes-and-ladders wrap.
- Native, editable PowerPoint rounded rectangles and connectors; PDF uses equivalent vector shapes. The PDF and PPTX are generated from a single structured source; do not copy a screenshot into the editable deck.
- Default nodes: numbered stage, short stage name (<=38 characters), one readable description (<=100 characters). Detailed inputs, outputs, citations, and limitations are in machine-readable fields/notes or a follow-on explanation slide, not crammed into nodes.
- Straight one-way arrows. Diamonds are *not* allowed by the current `horizontal_linear` implementation; add a reviewed conditional-layout type only if an actual methodological decision is documented. The names `horizontal_swimlane`, `horizontal_grouped` and `horizontal_feedback` are reserved **future proposals**, not implemented claims.
- Minimal neutral contrast compatible with white/Parchment PU slides and exact Times New Roman in final production; no decoration, dark fills, low contrast, slide overflow, or fake decision paths.

## Research semantic contract

1. Resolve the **current** manuscript commit and Chapter 3 method; every stage must trace to `manuscript_locator` and currently admitted `evidence_refs` in the project evidence map.
2. Mandatory each: `stage_id`, `title`, `description`, `category`, `output`, `manuscript_locator`, `evidence_refs`. Optional: `input`, `tools`, `notes`, `evidence_status`.
3. `stage_id` must be unique and durable; sequence uses JSON order. `connectors` may be omitted for automatic adjacent arrows; if supplied, they must precisely connect adjacent stages with no cycles or unreferenced IDs.
4. Machine admission is not methodological/scientific truth. An existing reference or photo does not prove that the stage was completed, a repair occurred, or a cost/delay was established.
5. Do not turn suspected construction defects into verified rework. Rework classification requires evidence of **original executed work + subsequent corrective intervention**; cause and impact are separate checks.
6. No fabricated number of cases, sites, surveys, samples, causes, costs, days or frequencies. Missing measurements are **unquantified**, not zero.
7. Title/description length and required fields fail closed. Researcher-only content changes must never hardcode source-specific text inside the shared Python renderer.
8. Full PDF/PPTX structural QA + rendered slide inspection, source/asset and exact-font validation remain separately mandatory; a synthetic test does not certify a researcher's scientific content.
9. Previous researcher output and scientific authority remain immutable until an independently enumerated release passes A9 PRE/POST and authorized review.

## Scientific approval boundary

The `a9_methodology_flow.py` gate checks layout choice, required fields, flow topology and admitted source links. It **cannot verify** that a person actually performed a stage. Researcher/supervisor must approve the sequence, the wording, and verification status. A candidate methodology file is **not an instruction** to mutate the manuscript or regenerate an already released PPTX/PDF.

## Change control

Global code, schema, tests, design and policy: **one** existing `controls/presentation/` shared tower, GitHub version controlled. Research-specific stages: `researchers/{slug}/presentation/methodology_flow.candidate.json`, referencing shared schema/handler. Private evidence-map content remains in authorized Drive. No cross-researcher scientific content or copies of the shared engine inside researcher branches.
