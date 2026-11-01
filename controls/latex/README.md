# THE SINGLE R&D LATEX CONTROL TOWER — 2.6.2

**There is one canonical operational owner:** [tower.json](tower.json) on R&D `main`. [pumlsc-shared.sty](template/pumlsc-shared.sty) is the one reusable template. Other JSON files in this directory are **subordinate modules of this single tower**, not separate authorities.



## University-source conflicts versus later user presentation directions\n\nThe original PU v1.13 format audit [PU rule map](pu-format-parity-audit.json) preserves the university-source wording as received, including dotted leaders in PU-FMT-024 and abbreviated Figure/Equation references in PU-FMT-035/041. The user's subsequently requested shared v2.6.2 presentation instead uses **dotless navigation** and full **Figure/Equation** designations. These are documented as separate user-directed display choices in the [authority conflict register](academic-format-conflict-register.json), not falsely certified as a university-endorsed change. The shared implementation is unchanged. Full 144-rule institutional acceptance remains a separate signoff.\n\n## Current common inheritance and navigation rules (v2.6.2, 31 October 2026)

- The ONE canonical shared style is `controls/latex/template/pumlsc-shared.sty`, currently **2.6.2** at Git blob `491538d53f83023af0b485dc0251728688ec4e2a`. Researcher versions pin the exact blob and must not maintain an independent template fork. Version history and global amendment `RD-LTX-CHG-120` are authoritative in `change-register.json`.
- The **dotless navigation** requirement now executes globally at begin-document through `\\PUEnforceDotlessNavigation`: no dotted leader trails in the table of contents, list of tables, list of figures, list of equations or list of appendices. Apply to newly built versions, not by rewriting previously accepted PDF archives. Confirm from the rendered output, not solely from macro source.
- Standard numbered section headings, for example `1.1 Background`, result from the researcher's `\\chapter{Introduction}` then `\\section{Background}` and the shared numbered-section formatting. The global style controls numbering, font and spacing. **Do not copy Saugat's Background text or require every researcher to use identical chapter text or headings** unless their own university/research outline requires it.
- Submission narrative follows semantic policy **v1.3.0** (`RD-LTX-SEM-001..013`): actual methods/results, meaningful tables, no internal audit-status prose disguised as research. Legitimate scientific limitations and mandatory assistance disclosures remain required. Source-specific scientific corrections stay owned by the researcher.
- Full PU formatting certification is **NOT complete**. The existing 144-rule source audit maps 144 requirements but records incomplete/unverified implementation, and any final PDF needs independent page-level format, typographic, equations, citations, permissions, approval and optional Google Docs parity checks when separately requested. A successful static source CI run does not close those gates.
- Saugat's SEQ029 was built with shared v2.6.1; SEQ030 migrates it to v2.6.2 and conducts a new exact-font navigation and semantic comparison while keeping the accepted M4 CURRENT stable until scientific and LaTeX/PDF release acceptance. These examples are evidence of a shared rule, not a universal assertion that all researcher PDFs have been rebuilt.

## Three connected controls; still ONE tower

The [tower.json](tower.json) on \`main\` is the **single machine authority** and researcher entry point. These are separate responsibilities **inside that tower**, not rival towers:

| Layer | Exact canonical file | Purpose |
|---|---|---|
| 1. Formatting | [pumlsc-shared.sty](template/pumlsc-shared.sty) | Reusable PU page/font/section layout; does not author scientific prose |
| 2. Manuscript semantics | [authorial-voice-policy.json](authorial-voice-policy.json) | Authentic research voice, evidence/causation, human-readable captions, citations, ethics |
| 3. Technical validation | [check_authorial_voice.py](../../scripts/latex/check_authorial_voice.py), [validate_shared.py](../../scripts/latex/validate_shared.py), [universal_preflight.py](../../scripts/latex/universal_preflight.py) | Advisory prose warnings, shared inheritance integrity and project-specific source preflight |
| 4. PDF QA | [qa-contract.json](qa-contract.json), [pdf_technical_qa.py](../../scripts/latex/pdf_technical_qa.py) | Exact fonts, references, all-page visual QA, source/PDF provenance |
| 5. Change and release history | [change-register.json](change-register.json) and [release-contract.json](release-contract.json) | Central numbered amendments, bounded release/Drive readback |

**Invocation for another researcher:**

\`\`\`bash
python3 scripts/latex/check_authorial_voice.py --self-test
python3 scripts/latex/check_authorial_voice.py --researcher nabin-bista --json
# Review warnings with the researcher; do not auto-rewrite science.
python3 scripts/latex/validate_shared.py
python3 scripts/latex/universal_preflight.py --policy-check
\`\`\`

The semantic checker is intentionally **advisory**; use \`--fail-on-warning\` only as an explicit review-team requirement. It cannot verify real field observations or certify university ethics/approval. First person is **not mandatory**, and genuine citations to other researchers remain third person. Never conceal writing assistance when institutional disclosure applies.

### Lessons generalized from Safal v1.11–v1.12

- Make the researcher's *own verified* field descriptions natural and context-appropriate, rather than calling the student an external "practitioner" or "the researcher" in every sentence; require human factual approval.
- Separate photographed site condition from verified repairs, causes, measured time and cost. Never synthesize missing case records.
- Keep private media IDs and administrative code names in evidence manifests / \`\\includegraphics\` paths, not printed captions.
- Excluding road work was **Safal-specific**; valid road research by another researcher must not be removed.
- The main PU style now offers an **opt-in** \`\\PUCoverLogoAuthorSpace[30pt]\` spacing helper. Safal's 30pt gap is not a new universal university requirement. This helper does not modify any existing cover unless deliberately invoked. Validate each title/cover page visually and against its approved university source.
- Source snapshot first, then build exact-font PDF and verify the provenance SHA; upload outputs into the owning Drive folders with provider readback; keep A9 and scientific approvals separate.

**Status:** Generalized semantic source rules and opt-in formatting API are reusable from the canonical tower. Independent full-document rendering for all other researchers and full PU 144-rule certification remain unverified; do not infer publication approval from a green code test.


## One template for every researcher

[registry/latex-inheritance.json](../../registry/latex-inheritance.json) enumerates all 12 registered researchers and points each to the **same exact template path**. Project metadata may change (name, stage, bibliography style, current source manifest, approved project-only extension), but formatting source may not fork.

The historical `controls/latex.control.json` file is an **alias only** and `controls/projects/safal-dawadi.latex.json` retains Safal's historic evidence/QA pointers for compatibility, **not an additional template**. R&D shares source; A7 only routes globally and owns no LaTeX tower. Drive remains the authoritative academic-original source until full parity, not a second executable tower in Git.

## A researcher's compiled-PDF discovery feeds the canonical template

1. Record the original visual/source issue and exact before/after evidence (private evidence stays in Drive).
2. Allocate the next `RD-LTX-CHG-101+` in [change-register.json](change-register.json); classify GLOBAL_CANDIDATE or RESEARCHER_ONLY.
3. Global correction: amend `template/pumlsc-shared.sty`, [core-rules.json](core-rules.json) and QA centrally; run validator and independent full render checks where available. Bump the canonical tower version and Git release after QA.
4. Researcher-only correction: register a reason/owner in [extension-registry.json](extension-registry.json), then add only the delta under the permitted researcher's `latex/extensions/` path. The base still comes from central.
5. If an exception later proves universal, promote it into shared template and mark original extension superseded. Every registered researcher then obtains it through the one shared path.

The `001..100` base and `101+` change numbering is an internal *illustrative namespace*: 15 actual shared rules currently exist; it does **not** claim 100 completed rules. It does not override separate original PU-FMT rule IDs.

## Safe production boundary

- No hidden universal citation style. IEEE/Harvard/APA7 selected in each project.
- Production exact Times New Roman from private licensed environment; compatible fallback is preview only.
- Editable source is canonical; fix source, recompile, run full-page QA. PDFs are immutable derived evidence in Drive.
- Passing source/CI tests is **not** scientific approval, production format certification, or A9 Main ACK.
- [Original PU v1.13](https://docs.google.com/document/d/1FjbNdNN_Fb_tKoapaYHW2jLoEF9lqxrYPYrCwTi87Ys/edit) remains format evidence until full parity, and [thesis control](https://docs.google.com/document/d/1jc6WIqXbAixAYYndeB2Idw59fAzjBbnDKlq49THeu_A/edit) remains private-source governance evidence.

### Single tower's implementation components

[tower.json](tower.json) · [core-rules.json](core-rules.json) · [PU rule index](pu-msc-format.rules.json) · [authorities](format-authorities.json) · [build contract](build-contract.json) · [QA](qa-contract.json) · [release](release-contract.json) · [amendment register](change-register.json) · [extension index](extension-registry.json) · [migration status](migration-status.json).

## Binding 2026-10-09 choices Q1B / Q2A / Q3A

Q1: Latest Safal v1.9 **Local seq15 reconciled target** selected. First-upload v1.9 ZIP/PDF are not the final reconciled hashes. Provider mirror/byte test pending, Git source admission HOLD.

Q2: Previous Git main SHA is PRE; one nonforced commit creates POST. Use **annotated Git tags** for major approved releases only, not repeated snapshot branches. Existing refs remain untouched. Tag-writing tool unavailable in this run; no new branch should be used to emulate it.

Q3: Admitted manuscript `.tex`, bibliography `.bib` and accompanying machine-readable source belong in the public R&D researcher folder. Build normal scholarly content from verified evidence, without internal machine-control notes in student-facing PDF; no unsupported scientific facts or references.

[**Complete inventory of 144 PU-FMT source rules and gap status**](pu-format-parity-audit.json): SOURCE INVENTORY audited 144/144, real format/font/whole-document production parity is NOT complete; PU-FMT-076 is absent in the Drive v1.13 original.

## Approved Memory Wall & numbered researcher workstreams (2026-10-30)

See [Memory Wall](../../docs/MEMORY_WALL.md) and [template inheritance/version protocol](../../docs/LATEX_TEMPLATE_INHERITANCE_VERSIONING.md). These point to this one tower; they do not create another one. New source branches inherit this exact shared template at their creation commit and pin its blob SHA in a researcher-only version manifest. Proposed global changes use a separate `template/latex/vX.Y.Z` PR, a `GLOBAL_CANDIDATE` amendment ID, source policy checks and independent visual regression before release. A new researcher sequence is NOT a global change-register ID or scientific CP checkpoint. The GitHub Actions reserve workflow defaults to no-write dry-run; unverified baselines fail closed.

## Submission results are not audit status (semantic policy 1.1.0; RD-LTX-CHG-115 candidate)

The public academic manuscript must communicate what was analysed, what the admitted results show, and what can legitimately be concluded. Do not insert internal source-availability grids, missing-data complaints, QA/AI self-narration, or objective-to-section traceability matrices as substitute scientific findings. Save internal evidence conditions and administrative links in the owning researcher's governed Drive Google Doc audit. Preserve significant methodological limits when necessary to avoid a misleading scientific claim; never invent analysis, imply a model parameter has been verified when it has not, or suppress mandatory AI-assistance disclosures. Student and supervisor approval remain independent of this semantic advisory policy.

Canonical semantic rules: `controls/latex/authorial-voice-policy.json` (RD-LTX-SEM-011..013), `controls/latex/core-rules.json` (RD-LTX-CORE-016). This is a **semantic control change**, not a modification to the shared PU `pumlsc-shared.sty` or another researcher's scientific manuscript. Any source rewrite requires a separately numbered researcher-specific version, PR, authentic provenance, full PDF build and scope review.

## Private Times New Roman resource and release order

The existing licensed four-face cache is owner-only: https://drive.google.com/drive/folders/1nf_nRgYbEXdA4xK7bhuA3tdgha8khvyv
Its provenance manifest is https://docs.google.com/document/d/1tX7hBF1DN-8llL2dBA-C08Ig5hs2npnRvS38X9qQSqY/edit . Use only during private builds, never redistribute fonts or copy them to public Git, source ZIPs, or deliverables. Production must explicitly resolve exact Times New Roman (regular/bold/italic/bold italic) and verify the output font inventory; `times.sty` silently selecting Nimbus Roman is a **review-only** fallback. Thesis deliverables follow the Drive-first, then Git registration, then optional native Doc export-and-parity steps only upon separate explicit request in `docs/RESEARCHER_DELIVERABLES_READ_FIRST.md`; failures remain HOLD and cannot be called final.
