# Saugat CP114 / LATEX_SEQ029 — actual provider and parity receipt

**Owner:** RSH-002 / Saugat Paneru. **Disposition:** SOURCE MERGED; 120-page exact-font candidate PDF and complete source filed on Google Drive; **native Google Doc/Latex parity HOLD**; current approved 115-page M4 untouched. **This is an internal QA artifact, not submitted manuscript text.**

## Authority and Git proof

- Original scientifically admitted checkpoint: CP114, accepted M4 remains CURRENT. Production CURRENT pointer: [Drive CURRENT_CHECKPOINT](https://drive.google.com/file/d/1vXh7XUbkZcqzI1q8GFxZ1EcFHUKZhKQN/view), original production PDF [M4](https://drive.google.com/file/d/1QLnRQrXQm9Y_gqrCLzcEjkht6MlXIkjk/view).
- [Protected-main reservation PR #89](https://github.com/FabinGurung/JP_Research-and-Development/pull/89), merge `470acacf5167719500b1d7dc5f11e15696f178d8`, historical seq028 → one seq029 reservation, preserved append-only history.
- [Test-fix PR #90](https://github.com/FabinGurung/JP_Research-and-Development/pull/90), merge `993ef1982594ed858d5e02d02a8587357e232be2`; removed a fragile hard-coded 029 fixture blocking legitimate next-sequence PRs.
- [Actual researcher source PR #91](https://github.com/FabinGurung/JP_Research-and-Development/pull/91), merge `34d5932af2480ca61624f9b385b2907a94db41eb`, all four source CI checks passed. Original `chapter4_results_discussion.tex` and `chapter5_conclusion.tex` byte-identical, 143/143 original binary research assets byte-identical. Four scoped owner `.tex` edits only: Introduction Background heading/order; source-grounded ETABS/program and model considerations; seven uncropped floor plans; GII numbering and List of Equations.
- Shared LaTeX **2.6.1**, same single shared `.sty` blob SHA `a8f1b332cfe90027f52ed180b81cda5553c21936`. No researcher `.sty` fork. Semantic policy **1.3.0**.
- The use of a GitHub connector to create reservation PR #89 was a **manual governed PR**, not a claimed GitHub Actions dispatch. No new scientific CP or approval inferred by the reservation.

## Actual file custody — original version remains immutable

All following candidate artifacts are filed under the actual [SEQ029 candidate Drive folder](https://drive.google.com/drive/folders/1aVKsAiAn63gPRPnsoSKD2sGEBeC0hCd8); this folder is NOT the permanent production CURRENT.

| Role | Verified Drive evidence | SHA256 / measurement | QA |
|---|---|---|---|
| Complete LaTeX source ZIP | [source ZIP](https://drive.google.com/file/d/1STUrm4KUqziu-yh8RZ7Lt4l2byN20x6E/view) | `a29e58b7b0c172a03b5fabac66893bf854bfe324fb63fa19e6fc7f918abba2bb`; 58,666,357 bytes, 232 entries, ZIP integrity PASS, 143/143 original binary assets intact | PASS as full review source |
| XeLaTeX PDF candidate | [120-page PDF](https://drive.google.com/file/d/1ONj5F_2RX0OR8sAeupBefjxZPfJk3SW8/view) | `980e73849ae787d61ffdb05e8bc6bfbdc0b5b847c981506af49cf03512bab86c`; 22,391,485 bytes; all A4 and nonblank; embedded TimesNewRomanPSMT/Bold/Italic | PASS technical font/render; NOT supervisor/institution acceptance |
| Full editable Word, revised 1.5 spacing | [Word review](https://drive.google.com/file/d/1UNtulxt0_S7dPLLQ0hNKHnL2cW0r7Jw2/view) | `cc7dc969eb35de0f5e4dad23ba237df1024feb41ac855b85e8429df07d2cb568`; 43,663,475 bytes, 40 native tables, 113 real images, 137 native math objects; Word render 108 pages | EDITABLE REVIEW, not exact PDF parity |
| Native Google Doc QA candidate (NEW, not permanent LIVE) | [native QA Doc](https://docs.google.com/document/d/1L-cNSoEmcy-wwLe33z5jvDea4pSqZ-GQ6-101R2vUU8/edit) | 40 native tables, 113 embedded images across paragraphs+tables, native text/revision, 150% paragraph spacing. Archived native PRE [copy](https://docs.google.com/document/d/1AJrV3U12wdnrGxGOtlK3C1W8CM-XKgo1nqn0fnLAC80/edit) and POST [copy](https://docs.google.com/document/d/13-B0-qSOJJQWPZwmzeao9GHfYHBTjQhtUpztZQ4vtIQ/edit). | CANDIDATE, native parity FAIL |
| Native Doc PDF export for visual QA | [109-page exported PDF](https://drive.google.com/file/d/1Fg5Vk0i5rpqPF13gHsBTiyWd_27MZNMC/view) | native export SHA `41419de6242ddf8ffd8fc2e8b4d6f049c5e13331a5f5efbe3a84243ec38e8546`; 109 A4 pages, Times New Roman embedded. | FAIL 109 pages versus 120 |
| Machine-readable parity receipt | [parity JSON](https://drive.google.com/file/d/1zcFTgFF0QYN9zVybfQuIhz5rxHBy6k7U/view) | Contains page, text and number comparison indicators; note initial Word ID in this earlier receipt was superseded by the improved 1.5-spaced Word above. | FAIL, not a false pass |

The existing populated native thesis live Google Doc [LIVE v1.1](https://docs.google.com/document/d/1P_4MFr3WDjkhg_vJQ0YRbqYGMSoUtqSAex-yEaxGgTs/edit) has **20 tables and 60 images** in the historical version. It has **not** been overwritten or repointed because the new 40-table / 113-image candidate fails whole-document parity. Audit and discussion Google Docs also keep their original IDs.

## Document-parity discrepancy and preservation

- LaTeX source PDF: **120 A4 pages**. Google Docs export: **109 A4 pages**. Editable Word review render: **108 pages**. Matching counts alone would not prove parity; this is a demonstrated failure.
- Extracted LaTeX text: ~161,624 chars; exported Doc text: ~135,710 chars; the numbers include layout and PDF-figure extraction differences. The full page-by-page content, citations, equation identifiers, captions and table values therefore **cannot be certified equal**.
- No credible provider-verified full 144-rule university acceptance or researcher/supervisor signoff is recorded. No change to M4 CURRENT, no new CP, no claim of completed results/discussion edits pending supervisor instruction.
- The four private Times New Roman faces were read from Saugat/A9 private build-resources only; no font assets were committed to GitHub, source ZIP or Drive submission deliverables.
- Pending to release: reconcile scientific exact text/data between LaTeX and native Doc, audit equations/figures/citations and page-by-page PDF export, restore in-place into permanent LIVE Doc only after authorized PRE/reconciliation, independently certify formatting, obtain supervisor/researcher acceptance, and perform governed CURRENT PRE/POST promotion. Never cover this deficit by adding blank pages.

## Restoration

Prior accepted CP114/M4 production PDF, ZIP and CURRENT pointer remain untouched. To roll back Git manuscript work, restore the source from the previous approved M4 commit/snapshot through a new protected-main PR; do not rewrite history. For native Doc, preserve the existing permanent LIVE ID and the PRE/POST candidate snapshot IDs; no RESTORE of LIVE is necessary because it was never changed. For a future release, archive PRE and POST for each live subject, preserve legacy refs and append exact provider/hashes to audit. This QA receipt cannot itself authorize a production release.
