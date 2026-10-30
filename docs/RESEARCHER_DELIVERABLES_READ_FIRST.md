# Researcher submission bundle and working records

User-authorized 31 October 2026. Rule **RD-LTX-CORE-017**, amendment
**RD-LTX-CHG-116**. The existing [Academic Writing tower](../controls/academic-writing/tower.json)
owns the [deliverable contract](../controls/academic-writing/research-deliverables.json).
This is a coordinating module, not another manuscript style or a duplicate evidence vault.
All registered owners inherit it through [enrollment](../registry/researcher-deliverables.json).

## The three manuscript deliverables

| Role | Deliverable | Release requirement |
|---|---|---|
| `submission_latex` | Complete editable LaTeX project, bibliography, build recipe, manifest and authorized assets; ZIP for delivery | Reproducible exact source, owner scientific revision, shared-template blob and asset checks |
| `submission_pdf` | Compiled thesis PDF | Exact required font/format, complete references, full-page rendered QA, owner authorization and provider byte readback |
| `submission_google_doc` | Native editable submission Google Doc | The same scientific content and exact format/pagination as the matching LaTeX/PDF, independently verified through a Doc PDF export |

These are three representations of **one admitted scientific revision**, not three
independent writing histories. Keep scientific checkpoint, source-tree SHA256,
Git commit, template blob/version, provider IDs/revisions and output hashes linked
in the owner's private release receipt. DOCX-first work is a precursor; do not
pretend an uncreated LaTeX project exists.

The submission Doc must not be the audit or discussion Doc. A PDF embedded as
page screenshots does not satisfy native editability. Its title, front matter,
section order, paragraphs, values/units, equations, tables/cells, figures/captions,
citations, bibliography, cross-references, appendices, limitations and required
disclosures must match the admitted source. Preserve native structure where
supported; record any unavoidable element limitation honestly.

Exact format includes institutional rule mapping, paper/margins, fonts/sizes,
spacing, headings, headers/footers, roman/arabic numbering, page and section
breaks, TOC/list of tables/list of figures, equations and illustration placement.
Export the native Doc to PDF, inspect **every page** against the exact compiled
PDF, compare page count and corresponding page content, and record both PDF
hashes and the Doc revision. Determine comparison criteria from actual format
authority; do not invent tolerances or substitute a source-lint pass for rendering.

Unsupported Google Docs features or pagination drift must be repaired or keep
that representation's parity/readiness on HOLD, with the precise discrepancy in
the owner's audit. A faithful content copy, a successful import, matching page
count alone, or a fallback-font preview is not exact-format QA. This policy
does not claim that a universal lossless LaTeX-to-Google-Docs converter exists.

If a human changes the submission Doc, reconcile the proposed edit into the
owner LaTeX source and repeat the affected checks. No silent last-writer-wins
overwrite. Any source, template, native revision, bibliography, asset or exported
PDF change invalidates the corresponding parity evidence. Each representation
has its own readiness; mark the bundle ready only when all three pass at the
same revision. Preserve accepted CURRENT until the separate release gate passes.
Technical readiness is neither actual institutional acceptance nor proof of submission.

## Presentation source and deliverable

The existing Safal Dawadi principle **is already in main**:

- Machine-editable source: **UTF-8 JSON** content, theme, methodology and evidence references.
- Generator: **Python `.py`**; shared code stays under `controls/presentation/generator/`.
- Editable slides: **`python-pptx`** creates native editable `.pptx` objects.
- Presentation PDF: **ReportLab**, using the same structured content and evidence lineage.

Read [Safal's existing governance](../researchers/safal-dawadi/presentation/GOVERNANCE_READ_FIRST.md),
[shared presentation tower](../controls/presentation/tower.json) and
[shared source guide](../controls/presentation/generator/LITERATURE_TABLE_READ_FIRST.md).
PPTX is an Office Open XML ZIP container, not a programming language. JSON plus
Python is the easy-to-edit source layer. The historical TypeScript/PptxGenJS stack
is not the current active engine. Do not reintroduce it as though it were deployed.

The defense deck is a distinct presentation, not a fourth identical copy of the
thesis. Its claims must trace to the same owner's admitted science. Preserve
editable native text, shapes, connectors and tables; screenshots of entire slides
do not satisfy editable-deck QA. Review the deck and its PDF independently.

## Separate working records

| Role | File | Purpose and boundary |
|---|---|---|
| `audit_google_doc` | Native Google Doc | Provenance, QA, limitations/data requests, displaced internal matrices, decisions and release evidence |
| `discussion_google_doc` | Native Google Doc | Discussion, supervisor feedback, original messages/source links, open questions and source handoffs |
| `analysis_notebook` | Google Colab `.ipynb` | Reproducible analysis with code/Markdown cells, pinned environment, source hashes, units/seeds, logs and durable restart checkpoints |
| `intake_google_sheet` | Native Google Sheet | Human data intake with stable row IDs, units, provenance, validation/admission status and separated input/formula/output ranges |

A notebook is JSON with executable cells; it is not proof that those cells ran.
Long sessions must checkpoint to authorized durable storage and resume safely;
do not promise uninterrupted Colab runtime. Record run IDs, exact inputs, code
revision, parameters, outputs/hashes and execution status. Keep credentials out
of notebooks and public Git; strip sensitive outputs before any approved code export.

The intake Sheet remains the human source for its designated fact class. JSON,
CSV and Pages are derivatives; do not overwrite original intake with generated
answers. New rows enter the manuscript only after source/units/calculation QA
and scientific admission. Actual empty/missing resources remain undiscovered;
do not create a blank Doc, Sheet or notebook merely to claim enrollment.

## Permanent identities and numbered archives

Follow A7's [permanent live-ID policy](https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/blob/ae0d8481f7a514ce838af4eec456024d1674bcaa/registry/curations/memory-live-version-control.v0.1.json)
and [version-control procedure](https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/blob/ae0d8481f7a514ce838af4eec456024d1674bcaa/docs/JP_A7_VERSION_CONTROL_READ_FIRST.md).
A7 is read-only for this task; R&D owns this implementation.

1. Discover and read the **original populated live file** and its actual ID/path,
   revision, name, ownership/access and hash where available.
2. Allocate the next ordinal in **that subject's existing central archive**.
   Copy `000001_PRE_<subject>` before a meaningful mutation.
3. Edit the **same live ID/path**, preserving the live name and unrelated structure.
   Use provider revision guards; reconcile concurrent human edits instead of overwriting.
4. Validate, read back the same provider ID/revision, and save matching `000001_POST_<subject>`.
   Verify it corresponds to the validated state; record provider-copy limitations.
5. Maintain a readable manifest and append-only version history with owner, live
   identity/revision, PRE/POST ordinal/IDs, what/why, original source links, checks,
   readback, unresolved issues and restoration instructions.
6. Restore old contents **into the same live ID/path** through a new governed event.
   Retain archives; never repoint all links to an archive as the new live file.

Each of the three thesis representations and each supporting subject keeps its
own identity and archive ordinal; link them by a release bundle without forcing
equal version numbers. Native revision history supplements the explicit archive.
Initial creation after verified absence has no fictional PRE: populate it, verify
it, record creation and initial POST. Preserve existing immutable candidate and
release IDs as history. A stable live manifest resolves which accepted artifact
is CURRENT; do not retroactively repoint accepted releases.

Git commits/PRs are the source PRE/POST history under the existing scoped Git/Drive
authority; do not make a Drive duplicate for every Git commit. Do not force-push,
invent legacy A9 ACKs or equate Sheet/notebook/archive/Git/CP/LaTeX counters.
Real private manifests and source content remain in authorized custody; public
Pages shows only permitted metadata, never newly exposed evidence or access controls.

## Execution and checks

Read live owner sources and [the engine procedure](RESEARCHER_ENGINE_READ_FIRST.md),
then inspect all roles, reconcile versions, reserve any genuinely new verified
LaTeX sequence, pin the shared format, and work in the owner's scope. Derive the
submission Doc from the exact admitted manuscript, run the parity checks, verify
provider outputs and stage a separate candidate. Apply the same semantic policy
to all submission-facing representations; keep internal narration in the owner audit.

Repository checks:

```bash
python scripts/researchers/validate_deliverables.py
python scripts/researchers/test_deliverables.py
```

Optional **private** evidence-consistency check:

```bash
python scripts/researchers/validate_deliverables.py --manifest /private/owner-release.json
```

The [receipt schema](../schemas/researcher-deliverable-release.schema.json) and
validator reject missing roles, stale hashes/revisions/template pins, aliased
submission/audit/discussion IDs, absent gate evidence, page mismatches, incomplete
bundles, cross-owner paths and replacement live IDs. Version events must cover
the receipt's `changed_roles`. For a native Doc, `artifact_sha256` is a documented
deterministic normalized native-content digest; record native revision and both
export/reference PDF hashes separately. It is not an invented native-file byte hash.

The validator tests receipt consistency, **not** the truth of external evidence.
It does not create Docs/Sheets/Colab files, fetch providers, convert LaTeX, render
PDFs or declare scientific approval. All 12 enrollment records begin UNVERIFIED;
they do not upgrade existing artifacts, release pins, data or CURRENT. Real
provider creation, long-session execution, parity QA and release are per-owner
operations with separately inspectable evidence.

Use the [general resume command](../prompts/RESUME_RESEARCHER_DELIVERABLES.md)
in each existing researcher thread. Other chats do not automatically refresh.

## Mandatory Drive-first thesis publication and private font cache (2026-10-31)

**Release order is mandatory, not an optional suggestion.** For every researcher, publish the versioned complete LaTeX ZIP and compiled PDF to the researcher's canonical Google Drive storage **before** claiming a Git release. Read back actual provider file IDs, sizes, MIME types and parents; then record those exact immutable release references and local hash distinctions in Git, run PR/CI/Pages readback, and only then certify any release step. This rule is also recorded in `controls/academic-writing/research-deliverables.json#drive_first_publication_gate`. Missing Drive readback **blocks publication-complete status**. A review candidate may be registered after Drive upload but must remain REVIEW_ONLY.

The native editable **submission** Google Doc is independently required. Its existence is not a parity certificate: compare its exported PDF to the exact compiled reference page-by-page, including text, figure/table/equation structures, pagination, margins, and font. If it cannot be made identical, keep the **submission Doc and bundle on HOLD**, without mislabeling it as approved. Git source checks alone never execute a native Docs conversion.

**Production font locator:** owner-only [Times New Roman private build cache](https://drive.google.com/drive/folders/1nf_nRgYbEXdA4xK7bhuA3tdgha8khvyv), with provenance in [font resource manifest](https://docs.google.com/document/d/1tX7hBF1DN-8llL2dBA-C08Ig5hs2npnRvS38X9qQSqY/edit). Four faces are present. This is a restricted build dependency, **not a public distributable font asset**; do not copy font binaries into source ZIP, GitHub, public Pages or submissions. Exact Times New Roman must be resolved for the chosen TeX engine and verified from the produced PDF's font inventory. `\\usepackage{times}` and Nimbus Roman do **not** satisfy the exact-font gate.

**Proven failure example:** Nabin LATEX_SEQ057 was first delivered as a local 89-page review PDF and ZIP without Drive/Git/Doc release. Those two files and QA were subsequently uploaded to Drive as REVIEW_ONLY. The PDF embeds Nimbus Roman, so exact production typography and native Google Doc parity remain unverified. This omission is a release orchestration failure, not a problem with user instructions.
