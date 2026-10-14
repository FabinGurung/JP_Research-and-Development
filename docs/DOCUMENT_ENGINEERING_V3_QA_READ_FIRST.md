# A9 Enterprise Document Engineering v3 - canonical candidates for human QA

## User instruction
Preserve all existing and historical `.tex` sources unchanged, make one callable template for each of fourteen document types, then compile fictional samples to PDF for human QA.

## Preserved original authorities
- Original private Overleaf ZIP (102 items): Drive ID `1wW-_B6bvETGFN_L7XMWcBZlUYBMTqzFP`, never modified or deleted.
- All original v1/v2 `.tex` files retain their existing Git paths and history.
- Immutable pre-normalization code ref: `snapshot/enterprise-v2-before-v3-normalization-20261012`, SHA `3a3fa4103797ae8dd601d5ec94aeff6b74ea03f1`.
- Existing v2 canonical registry remains the active registry, pending user QA.

## New candidate layout
- `registry/enterprise-document-v3-candidates.json` maps exactly 14 type IDs to one v3 `.tex` each.
- `templates/enterprise/v3/enterprise-v3.sty`: one shared A4 typographic system, 23mm horizontal margins, 25mm/23mm vertical margins.
- `scripts/document_engineering/engine_v3.py`: standardized call `template_id` + typed fields + source proof -> generated TeX and PDF + QA JSON.
- `examples/document-engineering/v3/*.sample.json`: fictional fixtures only. No real clients or verified financial amounts.
- `.github/workflows/enterprise-v3-preview.yml`: repeatable 14-PDF CI sample build.

### Running examples
```sh
python3 scripts/document_engineering/engine_v3.py --self-test
python3 scripts/document_engineering/engine_v3.py --demo-all --out /tmp/a9-v3 --compile
# Private project task - never run with real inputs in public CI:
python3 scripts/document_engineering/engine_v3.py --data /private/input.json --out /private/draft --compile
```

## Important boundaries
Every generated PDF is **a draft pending human QA**. Compiler success, correct page dimensions and readable text do not mean legal correctness, confirmed project scope, employer obligations, government-tender eligibility, accurate CAD takeoff or true financial transactions. The v3 engine rejects unregistered IDs and missing fields and requires authenticated private source context for non-fixtures.

Do not use `v3` for production yet. First inspect the fourteen PDFs side-by-side with the source archive and explicitly approve each family or request corrections. Only then route the canonical registry to v3 without deleting historic templates.
