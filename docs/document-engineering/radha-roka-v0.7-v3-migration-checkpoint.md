# 07_Radha_Roka — v0.7 migration to the canonical Enterprise v3 client-contract

**Checkpoint:** 2026-10-16 | **Status:** compiled and technically compared; still an unsigned project draft.

## One active callable template
- v3 Enterprise canonical ID: `client-contract` (alias: Construction Works Agreement).
- Canonical source: `templates/enterprise/v3/client-contract.tex`, approved source Git blob `c362c5d11a6a483ef13ac2ec14b6c09391da5013`.
- Shared style: `templates/enterprise/v3/enterprise-v3.sty`, Git blob `e4045844479365090b349f6f0451720fa47a1e07`.
- Release tag: `a9-enterprise-docs-v3.0.0`.
- The private v0.7 master is a **project instance derived from that canonical v3 source**, with a Rohini brand/formatting overlay and the existing private `contract-content.tex` source.
- It is NOT another template choice in the registry. No v3 canonical .tex, company standard letterhead, or original project revisions were modified.

## Verified prior revision (v0.6)
- PDF: https://drive.google.com/file/d/1_A_k28ibt3lkdOuxi6LdBSU8rxnm753q/view
- Full sources: https://drive.google.com/file/d/1uAUOLq2Em2407wlhouf5aQKeJ1_rqkSX/view

## New private project revision (v0.7)
- Project folder: https://drive.google.com/drive/folders/1PgT3-drU7ZNzEij6tsdDVcofW40ZVxIr
- PDF: https://drive.google.com/file/d/1G8pWzGYnNG22eGIuiViD_9kD4LPkpbg2/view
- Editable master .tex: https://drive.google.com/file/d/1E3tvpawXmK4itgorPgtdCjdtDl-9JHcr/view
- Complete editable ZIP: https://drive.google.com/file/d/1zPWI0cdNEXLu0229dFHwTdgeWH56IqAu/view
- 4-page A3 side-by-side PDF comparison: https://drive.google.com/file/d/1y-W_F8HgBmRqaUE8Q3xoKjahNLx9Jnqy/view
- SHA / PDF QA evidence: https://drive.google.com/file/d/1CGM-XizK_U_UBph12_vk4Aax-eD4p4UA/view

## QA findings (comparison made against **live Drive v0.6 PDF bytes**)
- Four A4 pages in both versions; the company logo is only on page 4 in both.
- The complete private contract-content.tex is **byte-for-byte identical** in v0.6 and v0.7; its ten sections, scope, payment milestones, retention, defects, demolition/salvage, and Appendix A have not been rewritten.
- Text extraction differs only in three inserted footer pagination words `page`; actual contractual words unchanged.
- v0.6 PDF SHA-256: `a912216861f89774b571218e264377991a3c7d5bc45022427acfc6a7fb920dbc`
- v0.7 PDF SHA-256: `da6d82f2b116871ba1d0fdfaadcee8fb35c3da31b1286b084da22630917d83c6`
- Visual page comparison and LaTeX compilation pass. Differences are in the common enterprise-v3 style and typography.

## HOLD gates before contractual issue
Site address; execution/date and commencement/target completion dates; payment due days; tax inclusions; actual signed drawings/specifications Appendix A; authorized signing parties; notice and cure periods; demolition permissions and salvage title; structural/storey nomenclature and further engineering/legal review.

The v0.7 PDF is **NOT approved for signature** merely because its formatting and content preservation passed. Only the owning private Drive project contains live contract data; GitHub only contains reusable source and lineage pointers. Academic Writing and unrelated GitHub Pages/Actions source files are untouched.
