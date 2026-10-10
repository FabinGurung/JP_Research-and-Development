# THE SINGLE R&D LATEX CONTROL TOWER — 2.1.0

**There is one canonical operational owner:** [tower.json](tower.json) on R&D `main`. [pumlsc-shared.sty](template/pumlsc-shared.sty) is the one reusable template. Other JSON files in this directory are **subordinate modules of this single tower**, not separate authorities.

## One template for every researcher

[registry/latex-inheritance.json](../../registry/latex-inheritance.json) enumerates all 11 registered researchers and points each to the **same exact template path**. Project metadata may change (name, stage, bibliography style, current source manifest, approved project-only extension), but formatting source may not fork.

The historical `controls/latex.control.json` file is an **alias only** and `controls/projects/safal-dawadi.latex.json` retains Safal's historic evidence/QA pointers for compatibility, **not an additional template**. R&D shares source; A7 only routes globally and owns no LaTeX tower. Drive remains the authoritative academic-original source until full parity, not a second executable tower in Git.

## A researcher's compiled-PDF discovery feeds the canonical template

1. Record the original visual/source issue and exact before/after evidence (private evidence stays in Drive).
2. Allocate the next `RD-LTX-CHG-101+` in [change-register.json](change-register.json); classify GLOBAL_CANDIDATE or RESEARCHER_ONLY.
3. Global correction: amend `template/pumlsc-shared.sty`, [core-rules.json](core-rules.json) and QA centrally; run validator and independent full render checks where available. Bump the canonical tower version and Git release after QA.
4. Researcher-only correction: register a reason/owner in [extension-registry.json](extension-registry.json), then add only the delta under the permitted researcher's `latex/extensions/` path. The base still comes from central.
5. If an exception later proves universal, promote it into shared template and mark original extension superseded. Every registered researcher then obtains it through the one shared path.

The `001..100` base and `101+` change numbering is an internal *illustrative namespace*: 12 actual shared rules currently exist; it does **not** claim 100 completed rules. It does not override separate original PU-FMT rule IDs.

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


## Student-author voice and evidence semantics (proposed cross-researcher rule)

The canonical `pumlsc-shared.sty` controls typography and document structure. **It must NOT manufacture the voice, evidence, research method or conclusions of a student author.** The project manuscript owns that text.

See [authorial-voice-policy.json](authorial-voice-policy.json) and run the advisory semantic checker:

```bash
python3 scripts/latex/check_authorial_voice.py --researcher safal-dawadi
```

Before release, a student must review the Abstract, Introduction, Methodology, Results, Conclusions and EVERY figure caption. Replace irrelevant phrases such as "the researcher observed" or "practitioner-reported" when those words refer to the student writing their own research; natural first-person past-tense statements may be appropriate if the university/supervisor permits. Do not mechanically change references to other investigators or make unsupported "I measured/verified" claims. Never print private `SAFAL-PHOTO-...` identifiers or internal case codes in the thesis; retain them in the source mapping and private photo register. Preserve accurate AI-assistance disclosure. **Scientific/authorial claims need student approval; the typography template cannot certify them.**

**Version discipline:** new scientific/content edit => new source version/ref and provenance manifest before production PDF. The PDF is a derivative, not the primary file. Never overwrite the previous source snapshot, force-move an approved release, or use an unverified local preview as the official university build.

**Status:** This shared guideline is on a researcher-reviewed PR branch until the shared LaTeX owner approves and merges it. Do not label it active for all researchers prematurely.
