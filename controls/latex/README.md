# THE SINGLE R&D LATEX CONTROL TOWER — 2.3.0

**There is one canonical operational owner:** [tower.json](tower.json) on R&D `main`. [pumlsc-shared.sty](template/pumlsc-shared.sty) is the one reusable template. Other JSON files in this directory are **subordinate modules of this single tower**, not separate authorities.


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

[registry/latex-inheritance.json](../../registry/latex-inheritance.json) enumerates all 11 registered researchers and points each to the **same exact template path**. Project metadata may change (name, stage, bibliography style, current source manifest, approved project-only extension), but formatting source may not fork.

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
