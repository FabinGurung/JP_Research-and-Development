# Saugat Paneru — M4 S03 full printing proof QA (2026-10-30)

**Production-admission boundary:** This is an evidence-grounded print-proof artifact. It does not establish signed university acceptance, 144/144 format certification, researcher-only authorship, or an independently revalidated ETABS engineering model. M2/M3 and CP114 remain recoverable.

## Final compiled printing artifact

- [115-page A4 exact Times New Roman PDF](https://drive.google.com/file/d/1moSo_vOrPikNDvNfJ_2Psq0MDTHqZs_e/view), 55,176,483 bytes, SHA-256 `ae62664f3bc3deac851e04d02c84f465a4d8ab0bd9b5cbb05c2fad5d3ec0340f`.
- [Complete editable source ZIP](https://drive.google.com/file/d/19mNSSYrDX5T47jocoJHCE9AGl3Fe3CLt/view), 58,660,829 bytes, SHA-256 `d9e53c4fa487d14e8f224489b852330a1e09e15472230f3c96770a4fb1ffd71d`.
- [QA report JSON](https://drive.google.com/file/d/1aZ6EgoYW6ng6kr8H67AGQW37p6kE8SyQ/view) and [Drive folder](https://drive.google.com/drive/folders/1LERNRdeKo_JFZEC1MyZYK47ZUrlkxibe).
- PDF and ZIP both independently re-downloaded from provider and SHA-256 matched, **not** only copied/metadata checked.

## Improvements since M4 source candidate

1. Replaced the generic Saugat certificate with the current shared certificate-page signatory layout from the [latest A9 certificate folder](https://drive.google.com/drive/folders/1nvGqhVH2sz7TzZ7o56Qu99JfeWASVF4g), adapting only Saugat's current scientific title and its available panel names; preserves signature/date lines and one-page certificate.
2. Uses `Er. Devendra Man Palikhey` according to the user-supplied shared A9 certificate, now consistent on title/administration pages. This is user-supplied institutional-template wording **not independent credential certification**.
3. Removed unsupported `Kathmandu University` organization assertion from Saugat's source configuration and recommendation (no replacement institution guessed). No alteration to historical signed originals.
4. Rephrased the introductory methods discussion to flow from equivalent static to response spectrum to nonlinear static analysis before presenting actual case results in Chapters 3 and 4.
5. Preserved M4 S03 source-backed Abstract, Conclusions, GII expansions and original three-method conceptual TikZ figure. **No underlying research dataset/analysis/figure was changed.**

## Print and technical QA

- XeLaTeX four passes, Biber, then xdvipdfmx; exact private Times New Roman, 115 A4 pages.
- Original assets: 143/143 source binary files SHA-256 identical to the earlier M4 source archive. Original 81/81 embedded image placements present.
- All 115 pages processed for text-bounding-box and nonblank-page checks. Zero text spans off the media page; zero overfull, fatal LaTeX errors, undefined references, undefined citations and oversized floats.
- Cover/title, certificate, recommendation, abstract, methods figure, main tables/conclusions and references checked in rendered pages; all pages generated as thumbnail contact sheets for overview. PDF preflight: valid, unencrypted, opens normally, not scanned-only.
- Inherited 252 underfull boxes and some sub-10pt original chart labels remain tracked as issue #34 rather than misrepresented as fixed. Scientific issue #35 unresolved; no new model science admitted.
- Full paper flow: five demand cases intact; seven main 3-storey plus stair cover distinct from separate four-storey; no categorical RUD expansion claim; CM–CR not treated as torsional classification; first peak versus performance point and final-step hinge observations kept separate; 18 failing frames for Soil D/Z=0.35 retained from admitted model records.

## Non-destructive Drive certificate-folder cleanup

- [Archive: older combined v1.0/v1.1/v1.2 PDFs](https://drive.google.com/drive/folders/18uS2Mtw7NAD_ye6CijllNbSHQH3TDnTw): 3 historical files moved with stable IDs.
- [Archive: older PRE/POST and superseded closeout files](https://drive.google.com/drive/folders/1f2Lfu92VdFaKAFVrby8ChYiDAEYGGDTR): 33 historical files moved with stable IDs.
- Shared `01_SOURCE` template, `00_A9_CONTROL` CURRENT files and 6-researcher combined `CURRENT` PDF remain unmodified; no cross-researcher content changed or deleted.

## Print instructions and unclosed factual gate

Print A4 at actual size/100%, not fit-to-page; proof-print first/second, certificate, a detailed chart, and conclusions. Signature/date fields are intentionally empty for authorized signers. Personal professional credentials and institution must be confirmed by the signatories before signed submission; no independent institutional proof was found. Researcher review of final prose remains required under S03-05.

**Prior M3 CURRENT:** [GitHub M3 release](https://github.com/FabinGurung/JP_Research-and-Development/releases/tag/saugat-cp114-m3.0.0-editorial-production-20261021). GitHub branch must be merged, and Drive CURRENT updated only in a separately provider-verified promotion step; this read-first does not itself claim promotion.
