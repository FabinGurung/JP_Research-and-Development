# Academic thesis presentation control — A9 / Pokhara University

One shared presentation engine lives under `controls/presentation/generator/`. **The manuscript is LaTeX; the presentation is Python** (ReportLab PDF + python-pptx editable PPTX). The Drive A9 presentation tower v2.2 remains the academic/source authority; GitHub versions executable code. Do not create a new presentation tower per researcher.

## Authority and source-first workflow
- [A9 Presentation Tower v2.2](https://docs.google.com/document/d/1i2YO58HJ1WVsYnBDP0a0ZJg-29VOPccPnWiWit08ofM/edit)
- [Presentation READ FIRST](https://docs.google.com/document/d/1uEw_cnlq75uMER3U6Z-njFKDXf1kFfz8bghM3k4dQ2g/edit)
- [Machine-rule registry](https://docs.google.com/spreadsheets/d/1q9gz1e8sdJkOo8U-ZpvglDOqHVw1N2_N3TkVqy6JCiY/edit)
- Canonical Drive generator v2.1 original SHA256 `fce6266ed54e724ce049909051f110bd0d99ea638cda65979cc1528f9da4d6b4`; active Git code incorporates subsequent approved patches.
- No private researcher photographs, citation PDFs, licensed font binaries, or generated PPTX/PDF binaries belong in public Git.

## Reusable literature review tables (v0.1)
The default is exactly **three columns**: Author (Year) · Key Finding · Relevance to This Study. An optional fourth column is Method / Limitation. The data and citations are passed as structured JSON, **not hardcoded** into the renderer. Long tables paginate automatically (up to three source rows per 4:3 slide).

Read in order:
1. `generator/LITERATURE_TABLE_READ_FIRST.md`
2. `generator/LITERATURE_TABLE_POLICY.md`
3. `generator/literature_table.template.json`
4. `generator/a9_literature_table.py`
5. `generator/a9_semantic_checker.py`, `generator/a9_presentation_validator.py`, `generator/presentation_schema.json`
6. `generator/a9_presentation_generator.py` and `generator/build.py`

Each row points to a `literature_references[]` item: verified author/year/title and BibTeX key, source ID, source kind, exact finding locator, and a separately justified relevance statement mapped to a manuscript objective. The semantic gate refuses missing/unknown or unadmitted source IDs, missing locators or unsupported source-to-project relationships. It **does not verify** that a paper truly supports a paraphrase; original-source reading and researcher/supervisor review remain required. Codes and product manuals remain distinguished from scientific literature.

## Developer test suite
```sh
cd controls/presentation/generator
python -m pip install -r requirements.lock.txt
python -m unittest -v test_a9_semantic_checker test_a9_literature_table
python smoke_test.py
python run_literature_fixture.py
```
The smoke test is **synthetic only**, never researcher evidence admission. Review 3- and 4-column renders, text layout, and editable native table cells. Production still requires exact Times New Roman, official PU logo >=2.25 in, supervisor metadata, semantic source map, PDF+PPTX visual QA and release/readback. Preserve researcher-specific scientific approvals and Drive Local/Main ACK state separately.

## Inheritance
Every research workspace `researchers/{researcher_slug}/presentation/` references this shared engine with only project-local content, current .bib, evidence-map IDs, and private assets. No Safal research claims or author findings are copied automatically to another researcher.
