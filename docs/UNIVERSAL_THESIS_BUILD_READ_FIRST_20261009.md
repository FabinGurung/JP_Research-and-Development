# Universal thesis Linux build · R&D v0.1

**Code artifact, not an automatic compiler service.** GitHub Actions must not produce PDFs on unrelated commits. Scientific source remains under owning researcher authority.

## Read order

1. \`registry/researchers.json\`; \`registry/researcher-folder-roles.json\`.
2. \`controls/latex/tower.json\` and \`controls/latex/pu-format-parity-audit.json\`.
3. \`registry/latex-build-profiles.json\`, exact owning project/source manifest and changed files.
4. \`controls/latex/pu-rule-enforcement-matrix.json\` for the applied test routes.
5. Technical validator output and actual problematic PDF pages only if formatting is being repaired.

**Source admission example JSON** (must be committed by the researcher owner, with real verified values and actual content SHA):

\`\`\`json
{
  "researcher_id": "RSH-002",
  "source_admission": "VERIFIED",
  "build_authorized": true,
  "selected_style": "controls/latex/template/pumlsc-shared.sty",
  "document_stage": "MIDTERM",
  "citation_style": "APA7",
  "main_tex_sha256": "<SHA256_OF_ACTUAL_MAIN_TEX>",
  "font_runtime_authorized": false
}
\`\`\`

The example is not itself authorization or a real project manifest.

## Deterministic calls

Install/provision Python 3.12, XeLaTeX, Biber, Poppler \`pdfinfo\`/\`pdffonts\`/\`pdftoppm\`, TeX Live package sources, \`git\`, and licensed fontconfig resources where applicable.

\`\`\`bash
python3 scripts/researchers/normalize.py --validate
python3 scripts/researchers/test_normalization.py
python3 scripts/latex/universal_preflight.py --policy-check
python3 scripts/latex/universal_preflight.py --researcher RSH-002 --manifest path/to/project-manifest.json --json
python3 scripts/latex/universal_compile.py --researcher RSH-002 --manifest path/to/project-manifest.json --mode preview --output-dir /tmp/rnd-thesis-review
# Only with explicit governing manifest:
python3 scripts/latex/universal_compile.py --researcher RSH-002 --manifest path/to/project-manifest.json --mode preview --output-dir /tmp/rnd-thesis-review --execute
# Authorized, exact licensed TNR review (still NOT university/submission certification):
RND_LATEX_FONT_DIR=/path/to/privately-licensed/fonts python3 scripts/latex/universal_compile.py --researcher RSH-002 --manifest path/to/project-manifest.json --mode exact-font-review --output-dir /tmp/rnd-tnr-review --execute
\`\`\`

The \`--execute\` invocation requires source admission and a real manifest. Nothing is inferred from a successful GitHub code check.

The runner always builds in a temporary Linux directory, resolves the **ONE** shared \`pumlsc-shared.sty\` via \`TEXINPUTS\`, runs XeLaTeX → Biber → XeLaTeX → XeLaTeX, inspects PDF dimensions/fonts, rasterizes every page, checks references and overfull boxes and saves a local candidate plus JSON metadata. It does not change Drive or A9.

Publication requires separate owning project approval; upload to governed Drive location; provider-read PDF and QA SHA; researcher Local ArtifactRegistry/ArtifactEdges/VersionLog/RunLog and checkpoint; only then independently authorized Main synchronization/ACK.

**Remaining:** Full 144-rule production compliance, independent visual inspection and licensed Times New Roman environment reproducibility remain separate gates. No live researcher is allowed to bypass unresolved scientific/administrative requirements.
