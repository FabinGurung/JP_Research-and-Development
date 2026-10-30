# Researcher artifacts and control alignment — 30 October 2026

**Not all manuscripts and PDFs are up to date.** The previous PR #71 audited governance, not all private artifacts. This audit inspected live main `286a88e7372d75940820bfe9b1a406b8ebcc529f`, discovered the additional Sandip registration in PR #72, read 11 verified project roots, inspected nine downloaded source ZIPs, and updated operational documents without replacing scientific text or accepted CURRENT.

Current formatting authority: `controls/latex/tower.json` / canonical shared style v2.4.0, blob `6fb77b6f09773e29bd1159a4dc4ec2d7f773aa06`. Current semantic policy: v1.1.0, RD-LTX-SEM-011–013 / RD-LTX-CORE-016. Existing released artifacts retain their tested provenance; a pointer update does not make them retroactively template-compliant.

## All 12 owners

| Researcher | Artifact baseline | Executed source finding | Remaining status |
|---|---|---|---|
| Fabin Gurung | v0.9 working | Local formatting; no shared-style import | Migration pending |
| Saugat Paneru | M4 CURRENT; M4.2 draft | M4.2 recovered style exactly matches main | M4.2 fallback-font preview filed and byte-readback verified; no CURRENT promotion |
| Nabin Bista | SEQ056 separate compilation | Local preamble; no shared-style import | Migration and PDF regression pending; stable CURRENT preserved |
| Safal Thapa | No verified artifact/root | Not testable | Owner/source identification required |
| Shisheer KC | CKPT14; CKPT15 phase4 candidate | CKPT14 uses local pu_fst_thesis style | Candidate reconciliation and migration pending |
| Binay Karki | R10.1 working; R10.2 preview | R10.1 complete ZIP: no shared-style import | R10.2 reconciliation, migration and PDF regression pending |
| Anil Neupane | R2.3 review candidate | No shared-style import | Migration and PDF regression pending |
| Rupesh Man Pradhan | v0.2.3 | Local-format monolithic TeX | Migration and PDF regression pending |
| Krishna Kumar Gupta | v0.3.5 | Local formatting; no shared-style import | Migration and PDF regression pending |
| Safal Dawadi | v1.12 review package | Shared style included, but bytes differ from main | Git/package source reconciliation, explicit pin upgrade and PDF regression pending |
| Sunil Rana | DOCX-first v0.1 + candidate | No admitted LaTeX project established | DOCX scientific recovery remains separate from future LaTeX conversion |
| Sandip Gurung | DOCX-first; registered RSH-012 | No admitted LaTeX project established | Registration reused; discussion/audit populated; no duplicate researcher |

## Executed changes

- Updated 13 existing native working/discussion/audit Docs in place. Readback compared the full original text with the original following the inserted addendum; original text was preserved. PRE/POST snapshots are in owner project-control `99_ENGINE_SYNC_ARCHIVE` folders. This is a separate ENGINE_SYNC event namespace, not a new scientific CP, discussion sequence, or LaTeX allocation.
- Populated six new operational Docs for Rupesh, Krishna and Sandip where no current native discussion/audit destination was established in the inspected role locations. These supplement original scientific records; they do not supersede an uninspected historical scientific audit. Verified their content (allowing the native trailing newline), native MIME and project parent. Initial POST snapshots retained; there was no previous populated document to snapshot as PRE.
- Reused Sandip's existing RSH-012 identity and existing source/PDF IDs; no duplicate enrollment or LaTeX conversion.
- Reconciled Safal Dawadi's previously null registry discussion pointer to his existing populated current Doc.
- Recovered Saugat M4.2 from existing artifacts, verified its two hashes, ZIP integrity and exact live style bytes, then filed it in his existing candidate folder. Independently downloaded both newly filed Drive files and verified SHA256 again. **No new compilation occurred in this run.** Its earlier 114-page fallback-font QA remains historical evidence, not an exact-TNR certificate.
- Added separate candidate pointers and Doc links to the registry; preserved all original working and CURRENT identities. No scientific source, shared style, result, sequence allocation or production promotion changed.

## Saugat candidate custody

- [M4.2 source ZIP](https://drive.google.com/file/d/14z5qlGkgLL2Gkg94nrQ5mxaoPRYY8uA7/view): 58,665,013 bytes; SHA256 `8e7427b961a5e021d166cb45fd4840b984379f1d45dc6c8ef6e0a550141d3d98`.
- [M4.2 114-page fallback-font PDF](https://drive.google.com/file/d/1xMlRg5UmibEqUEv_wR1v1DYfdCp1rwmg/view): 55,056,416 bytes; SHA256 `81cebc8f0fffbaa6d7f76f21012b183353832297aa09e4be39c8fa4f6fb6eb67`.
- [Owner editorial/evidence audit](https://docs.google.com/document/d/15IK5qfu4143tpVZpCXfFY-o2pQY5qkkyW9wzVH5n5To/edit) and [draft PR #66](https://github.com/FabinGurung/JP_Research-and-Development/pull/66).
- Stable production CURRENT_CHECKPOINT `1vXh7XUbkZcqzI1q8GFxZ1EcFHUKZhKQN` was read and still identifies M4 S03; no mutation.

## Working Docs updated or populated

| Owner | Document | Mutation | Recovery |
|---|---|---|---|
| fabin-gurung | [Live Doc](https://docs.google.com/document/d/1ZnSSqwoOE7wCIWNrUBlCw8w43cqMVL3YRS9Dp1ot-jI/edit) | Existing text preserved; addendum inserted | [PRE](https://docs.google.com/document/d/1ds9BrNnf3ikztJDicpYuGqmjC_pzQcRdqwapypq5Jic/edit) / [POST](https://docs.google.com/document/d/1LWDDKvYOQj_pNzroBtylvQ3f7b8j9yGXxFQKR8OJYmA/edit) |
| saugat-paneru | [Live Doc](https://docs.google.com/document/d/1lF5WKoido1Tzgk6D9ZFLbkVjV3TCwZinrNnLfVF7bA0/edit) | Existing text preserved; addendum inserted | [PRE](https://docs.google.com/document/d/17ap-YEmnPti_WUfflyuYPePylB2PpYRIRS2Pfv8CVe4/edit) / [POST](https://docs.google.com/document/d/1a-tcd6Djy8qQQlh3HXzOmB-lRhbFXQlGUQOKSyxtrEo/edit) |
| nabin-bista | [Live Doc](https://docs.google.com/document/d/1eLsGVmUxMyHx0QKeQv25SiR325c8jy3grfdXmkkz9xk/edit) | Existing text preserved; addendum inserted | [PRE](https://docs.google.com/document/d/1PSA4TRDM44Lb500DdQ57gu3e0JBUfYM4Rbg_2q_ZQLk/edit) / [POST](https://docs.google.com/document/d/1HM9WobzcIRCJ1S1audT0Ihh5IyMfr_QYDDfd8UQMipI/edit) |
| binay-karki | [Live Doc](https://docs.google.com/document/d/1wMU2eYikHZ8Bt4Qrvtqv8ITTtgiGUav4c-oMsVEMwX4/edit) | Existing text preserved; addendum inserted | [PRE](https://docs.google.com/document/d/1T4PumafucUCQDi0fjwNhLWc080A0oyXKhoXt9c3Jkbo/edit) / [POST](https://docs.google.com/document/d/1Y2Ne2LtkQawzzUn9QMnF9oMhqmJdpp8z39I3u8cKYFg/edit) |
| binay-karki | [Live Doc](https://docs.google.com/document/d/11EyRADuMW9ql_NhQTuFoop7BrPKFJmbBbJaMXFCt4Z0/edit) | Existing text preserved; addendum inserted | [PRE](https://docs.google.com/document/d/1Pp02JpLa4I481fdUspb9NQR4KQkwc8ijT6pMuHhBQek/edit) / [POST](https://docs.google.com/document/d/1BpDCPfHhty8JRLZFLm3oHhW0-S4JgSho-HLpGSjxN7w/edit) |
| saugat-paneru | [Live Doc](https://docs.google.com/document/d/15IK5qfu4143tpVZpCXfFY-o2pQY5qkkyW9wzVH5n5To/edit) | Existing text preserved; addendum inserted | [PRE](https://docs.google.com/document/d/1mhTudXUXq9nTKBq9wN8B8SDETVrfdl4gHKlkgKP3yPg/edit) / [POST](https://docs.google.com/document/d/1OECdRaDYzd0PaDbSr0LwTiZ-lH-ezD5-BwiwVwjTFik/edit) |
| nabin-bista | [Live Doc](https://docs.google.com/document/d/1Eg8Hgnh9dxZi9K7vCb7FX7fuJNbKZGCzTnu7GFqCIfM/edit) | Existing text preserved; addendum inserted | [PRE](https://docs.google.com/document/d/1lcEm1XdIoH0Tod4-X4WYmch4wicjO7hZ6rSuM2wxjR8/edit) / [POST](https://docs.google.com/document/d/1MRS5Vx9CWlFL0AgNBlUhxdjCd3U0fXk-UoiDugqigCI/edit) |
| shisheer-kc | [Live Doc](https://docs.google.com/document/d/1cVhIunKP_hxba_UUw8g4KchqbLw02OjlrJcZlA9-ObQ/edit) | Existing text preserved; addendum inserted | [PRE](https://docs.google.com/document/d/15bwhMus9wRwAVbU6AEVJAjD_C3F6eILVRtOg8WJpMNs/edit) / [POST](https://docs.google.com/document/d/1NuvVQO8F76rs7cECXuDOK_UoJqaiXd2HsVnpd7eHDDw/edit) |
| anil-neupane | [Live Doc](https://docs.google.com/document/d/1pB3sVI1xfthQGK9SFDx9YkkV7FgpWZPUD0gsx4dhvKI/edit) | Existing text preserved; addendum inserted | [PRE](https://docs.google.com/document/d/1xcgjRQ8WdtyiBC3lkPk9BJhpTfIgImf4vise8DiZDZs/edit) / [POST](https://docs.google.com/document/d/1wRUGwkIxjWHFrAh9MKmfQRnlg85_G1DoSpX4Xlm_1_E/edit) |
| sunil-rana | [Live Doc](https://docs.google.com/document/d/1yE2FNlDbDTCMfjG5fH13LBcUoVSAhW523JqT2a4uQpg/edit) | Existing text preserved; addendum inserted | [PRE](https://docs.google.com/document/d/1zkCiKkWTmx0jdQndihqUg0xTYDAMXIvXrN0WETATlxQ/edit) / [POST](https://docs.google.com/document/d/1Qx0WL18bg7YcqzsWT_Gn6LuJQNtonTdxxModOgpoGBQ/edit) |
| safal-dawadi | [Live Doc](https://docs.google.com/document/d/1rDnYR9WelWIDCaIpmlZoKF6oTWNuySvUCqzfPp5sfVU/edit) | Existing text preserved; addendum inserted | [PRE](https://docs.google.com/document/d/1vj0BmCWvRzNq4B8P5vvU-dZxUcTryhodDDS_DZL3lww/edit) / [POST](https://docs.google.com/document/d/1DPgXCKwQWJYziil_xd079CaSpN38JY2z9a1I7xWmPzk/edit) |
| safal-dawadi | [Live Doc](https://docs.google.com/document/d/1f0wvHqjWH659FyYgNnvvjvWj-nvFRgdxW0XrhkhPCyk/edit) | Existing text preserved; addendum inserted | [PRE](https://docs.google.com/document/d/1b8DSnjH7oI60gVyvF6_G0AjDxtFQfYbQjikGBubhNO8/edit) / [POST](https://docs.google.com/document/d/1FiDODC6HqQMM8uCMp-zo2cg4BXofA38iS_KVSCi-1LE/edit) |
| anil-neupane | [Live Doc](https://docs.google.com/document/d/1VZG6kF-JPvNZEwAXr_AwKMt6mRdmZfJhScXyMHmdtfA/edit) | Existing text preserved; addendum inserted | [PRE](https://docs.google.com/document/d/1vkQUAQCVl4Wae8bYhdEDnuVOXYjWAWV6B3E97lIUBl4/edit) / [POST](https://docs.google.com/document/d/1wexRyCPB1kRJ3UqS0Z0J72mDaoQfHGtBms3qr6dT7e4/edit) |
| rupesh-man-pradhan | [New audit Doc](https://docs.google.com/document/d/1jFqm-JJBQdyxO77V3TwVhcDdducj0rmuwHL0NsfRpg0/edit) | Populated operational record | [Initial POST](https://docs.google.com/document/d/1RWRbBt6pZvoArLOzfrJW-VINjbvwaOqc0uHFfPmo4ks/edit) |
| rupesh-man-pradhan | [New discussion Doc](https://docs.google.com/document/d/1oWC4YJfoNHCv6CT0GkCe_Ikt6D23FFS7E929g1N7gQ8/edit) | Populated operational record | [Initial POST](https://docs.google.com/document/d/1LUnattJe3lC8bMf8mmaPw4tjak3P3Ym5bsNsgaLwSUg/edit) |
| krishna-kumar-gupta | [New audit Doc](https://docs.google.com/document/d/1TKFJGcSFbDmoiQJYcftOopsT7oCXB8ApSkV9VbLjqLg/edit) | Populated operational record | [Initial POST](https://docs.google.com/document/d/15JnuZchMRn5hloe8yOVQTcJekxYvzntxmK_z7RoVI4Y/edit) |
| krishna-kumar-gupta | [New discussion Doc](https://docs.google.com/document/d/1PvbvLLrgx6yUG4XHkICxq260TDuFN5USa-g_Oe9WWJI/edit) | Populated operational record | [Initial POST](https://docs.google.com/document/d/1CXJYd0FeyAPvNCTpAVThxW2nhvJlz_dqgCmmWBBYiJo/edit) |
| sandip-gurung | [New audit Doc](https://docs.google.com/document/d/1eKFQTFW1h9aWhCUAtsWTvyh-MbGjcy4z8bKNxFn38fI/edit) | Populated operational record | [Initial POST](https://docs.google.com/document/d/1m53dULx5frScU8DJJwgkqE2YGloCYxtB5o7v5zaGl74/edit) |
| sandip-gurung | [New discussion Doc](https://docs.google.com/document/d/1wScw2xkYyQngfZ-Ji72ux9IA_iBem3LAg_dZtuOFQNE/edit) | Populated operational record | [Initial POST](https://docs.google.com/document/d/1Omb-AAJEpdRSuwpWkTjOXrHZyR9uVq1anwafwrel3Jw/edit) |

## What is not certified or completed

This is not an all-researcher migration or scientific review. Seven inspected ZIPs have no canonical shared-style import; Safal's bundled style differs; Saugat M4.2 matches the style but remains a separate preview. Sunil and Sandip are DOCX-first and Safal Thapa has no verified root/artifact. This does not establish every preview as the latest authoritative source: especially reconcile Binay R10.2, Shisheer CKPT15 and Safal Git/ZIP divergence before editing.

Source advisory matches require contextual review, not automatic deletion. Complete package scans may include historical TeX as well as active content; counts are not a scientific verdict. No fresh full-page PDF regression or exact licensed-font build was performed here. No university approval, scientific result validation or unperformed analysis is inferred. Other artifact lanes (slides, datasets, notebooks, original model files) are preserved, not certified by this document.

The project sequence and admission gates still apply to migration: resolve each owner's authoritative baseline, prepare a separately versioned owner candidate, pin the shared style, preserve numerical/asset lineage, move displaced administrative prose to the same owner's audit, run the full build/visual/reference checks, file/read back source and PDF, and promote CURRENT only through the separate release gate. Unknown baselines remain unknown; no number is invented merely to make the table look complete.

The adjacent [JSON receipt](RESEARCHER_ARTIFACT_SYNC_20261030.json) records hashes, source paths and snapshot identities. It is dated evidence, not a second template/control tower. Future sessions must still read live authorities.
