# Safal RSH-010: 25-photo field-review module — 2026-10-10

**Review branch only. This is not an approved manuscript release, PU-format certification, or supervisor-approved scientific dataset.**

## Structure
- `chapters/chapter4_photo_w01.tex`: seven threshold-related photographs, followed by five other roof/finish observations.
- `chapters/chapter4_photo_w03.tex`: five masonry photographs, with contextual limitations.
- `appendices/appendix_external_pcc_photos.tex`: eight separately contracted/public-road PCC photos, retained only as a comparison and **excluded from RCC building rework results**.
- Existing chapter 4 and `main.tex` only gain `\\input{}` statements. Approved scientific chapters, equations, numeric claims, references and bibliography were not replaced.

## Private images
**DO NOT commit or mirror source photos to public GitHub.** Source image IDs `SAFAL-PHOTO-W01A-01` through `W01A-07`, `W01B-01` through `W01B-05`, `W03-01` through `W03-05`, `W02A-01` through `W02A-04`, and `W02B-01` through `W02B-04` correspond to the privately maintained photo register in Safal's Google Drive evidence folder.

The LaTeX source references `private_photos/SAFAL-PHOTO-*.jpg`, included only in a private authorized build environment. If absent, the template emits explicit *Private evidence image* placeholders: a successful source-only build **does not mean photos were included**.

The licensed official Times New Roman build is a separate private release dependency. Keep `\\usepackage{pumlsc-shared}` from the canonical R&D tower. The locally prepared temporary PDF preview used a different nonofficial fallback font and cannot be promoted as a certified university output.

## Scientific status and field claims
- Researcher identifies the door-threshold house as residential, Lamachur, Pokhara; no link to a specific Fishtail Builders project ID or legal client address is yet independently verified.
- The Fishtail operational Drive site-location list establishes *existence/identity of projects only*. It is not photo-to-project event attribution.
- Reported threshold removal, reinstatement, symptom, rainfall/use observation, cost records and diary entries remain respondent claims until a site-level readback.
- Masonry corrections and alleged missing concealed bands require distinct verified photos/drawings.
- Public road-PCC defect and joint photos are visual comparisons, **not building-contract rework cases**; the reported curing concern is not independently established.
- No measured rework costs, project delays, site counts or cause rankings are introduced by this branch.

## R&D template invocation
`PU LATEX TOWER — RSH-010 SAFAL DAWADI` is a conversational shorthand, not an intrinsic GitHub command. The actual source invocation is `\\usepackage{pumlsc-shared}` in `main.tex` with the canonical template made available to the TeX tool path. Recommended private-build sequence: XeLaTeX, Biber, XeLaTeX, XeLaTeX; compare rendered pages and verify fonts, citations and overflow before any release.

**Next gates:** researcher reads and corrects captions; site/photo mapping and client publication permissions; supervisor feedback; certified private Times New Roman build and all applicable PU format QA; A9 Local PRE/POST; Main remains HOLD.
