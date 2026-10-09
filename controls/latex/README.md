# THE SINGLE R&D LATEX CONTROL TOWER — 2.0.0

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
