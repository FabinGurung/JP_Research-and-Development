# Read first: literature review component

The presentation is built by **Python** (`reportlab` for PDF and `python-pptx` for editable slides). Manuscripts use **LaTeX**. These systems share source/citation authority, but presentation rendering is not LaTeX/Beamer.

- Template: `literature_table.template.json`
- Semantics, admission and pagination: `a9_literature_table.py`
- Content schema: `presentation_schema.json`
- Whole-deck semantic checks: `a9_semantic_checker.py`
- Structural validator: `a9_presentation_validator.py`
- Rendering: `a9_presentation_generator.py`
- Orchestration: `build.py`
- Guardrails: `LITERATURE_TABLE_POLICY.md`
- Tests: `test_a9_literature_table.py` plus legacy test suite
- Synthetic end-to-end example: `run_literature_fixture.py`

The table is content-driven and reusable across researchers. If you add a new paper, you should only amend project-specific structured content and bibliography/evidence map; do not edit the rendering code to add the author's name.

A 3-column table is the default. The 4-column variant is optional when a method/limitation warrants a separate column. More than 3 entries automatically paginate into follow-on slides. Rows referencing unregistered/unadmitted papers or missing finding and project-relevance locators fail closed. The validator does not establish scientific truth.
