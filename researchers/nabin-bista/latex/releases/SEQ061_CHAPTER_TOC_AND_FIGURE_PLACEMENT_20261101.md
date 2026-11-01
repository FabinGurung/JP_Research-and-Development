# Nabin Bista — LATEX_SEQ061: Chapter layout and figure-relocation update

This revision continues LATEX_SEQ060 in the same governed Drive PDF and source ZIP IDs. **No researcher scientific data or original figure bytes were intentionally replaced.** This is a scoped presentation and editorial revision.

## Verified changes
1. Abstract: shorter, source-based, single physical A4 page.
2. Removed duplicate hospital architectural plan from Chapter 3 (previous Figure 3.2). The same plan stays in Appendix 2, Figure 2.1. Current Chapter 3 figures were automatically renumbered contiguously.
3. Six Block 1–6 original 2D structural plans displayed two side-by-side on three pages.
4. 36 existing response/fragility images moved from their appendix-only placement to Chapter 4: 6 displacement plots in §4.3, 6 drift plots in §4.4, 24 fragility plots in §4.8. Original appendix TeX source remains in the ZIP as an uncompiled historical source, avoiding duplicate rendering.
5. Global shared style v2.6.3, rule RD-LTX-CHG-122, merged under PR #115. CHAPTER n and its title appear on distinct TOC lines; TOC chapter entries have no page numbers while sections retain page numbers.

## Permanent Drive IDs
- [SEQ061 PDF](https://drive.google.com/file/d/13beLy7N55TkgmMY1dzRpuK9hutmKFtjO/view), 93 pages; PDF SHA-256 `512119fe61de7da0cb3cb75318632560d1a5b328e32cffff94a0bf771e9a1fb5`.
- [SEQ061 source ZIP](https://drive.google.com/file/d/1XrUsz38STZ_2dliEOnxyNjlioYckuuKx/view); ZIP SHA-256 `ffb4701dc5861c4c742b3d96e9d2505ccf779e81b93d1328b54b3696f7281e2d`.
- [Permanent native Google Doc](https://docs.google.com/document/d/1AYv3p4rkL1XjvSfa1iiTmu0AqjdxZXEeQKXhiVvM6Qg/edit) is preserved but NOT revised to SEQ061; no three-format parity assertion.

## Numbered PRE/POST restoration
- 000007 PRE = SEQ060 [PDF](https://drive.google.com/file/d/1kpVL-aB0UxXW3NWwQe38MKf_yWYFmBh5/view), [ZIP](https://drive.google.com/file/d/1E5K6CrSlv5wqF6XcPVfEjhh7tFzLhoji/view), [native Doc](https://docs.google.com/document/d/1ulicYKGJ8tSLNA_tRrKtAbyjCX7an_JtEFTXkqn782I/edit).
- 000007 POST = SEQ061 [PDF](https://drive.google.com/file/d/1R5UVQtr5ChGsGLvk1kMi9no8DH_lwN_3/view), [ZIP](https://drive.google.com/file/d/1wf9NLBFKJtHHc4vlkZdhCEF4wP3tPt3V/view), [internal QA](https://drive.google.com/file/d/1KurgLdzUSFC3CX8nWH2SoH_3cVEWhlf3/view).

## QA and outstanding checks
- XeLaTeX + bibliography completed, 93 A4 pages. All 53 Chapter 4 figure captions appear once in consecutive sequence, and all 36 relocated figure records accounted for.
- Abstract occupies one page. Six 2D plans render two per page. TOC chapter entries do not display page numbers; sections do.
- All 340 inherited SEQ060 source entries retained, 320 byte-identical. Source additions limited to version metadata; original scientific images unchanged.
- Exact clean-room rebuild using GitHub canonical shared .sty was **not independently certified**: the compiled ZIP uses an explicit source-compatible implementation of the new TOC macro on top of the pre-existing populated manuscript preamble, while GitHub uses `\usepackage{pumlsc-shared}`. Canonical source should be fully reconciled on next production build.
- No native Google Doc regeneration or PDF-vs-Docs page-by-page parity, scientific approval or university-certified submission is claimed.
- Old raster labels embedded within Blocks 3–6 are not addressed by this scoped request.

For restoration, replace the bytes of permanent Drive live IDs using PRE copies and record a new corrective sequence; never delete POST.
