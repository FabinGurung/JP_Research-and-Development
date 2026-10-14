# A9 Enterprise Templates v3.0.0 — Approved Layout Milestone

User-approved on 14 October 2026: fourteen normalized, reusable enterprise document template **layouts**.
**Not** approval of private real-company contracts, statutory claims, payment values, client signatures or legal validity.

- **One active callable template per named document family:** registry/enterprise-document-types.json
- **No silent legacy fallback:** scripts/document_engineering/resolve_template.py
- **Renderer:** scripts/document_engineering/engine_v3.py
- **One shared A4 LaTeX style:** templates/enterprise/v3/enterprise-v3.sty
- **14 template sources:** templates/enterprise/v3/<canonical-id>.tex
- **Historical preservation:** registry/enterprise-historical-tex-sources.v1.json (19 pinned historical .tex blobs);
  earlier v1/v2 files unchanged, preserved in Git history and separate branches.
- **Original Overleaf ZIP:** 102-file private Drive original, ID 1wW-_B6bvETGFN_L7XMWcBZlUYBMTqzFP; unchanged.
- **Technical QA:** 14/14 fictional PDF builds, GitHub Actions run 38201154107.
- **Review booklet:** https://drive.google.com/file/d/1wN3fMKS5EW4xnOnLcnlgUxPX5se6C4jb/view
- **Individual QA PDFs:** https://drive.google.com/drive/folders/1JMx-NkWVIIzbMAg4gGB3UAnx8JCI6cLt
- **Scope guarantee:** no academic controls, researcher workspaces, websites unrelated to Enterprise Documents,
  or other Actions workflows are intentionally modified by this release.
- **Release gates:** domain accuracy, legal review where needed, authorizations, final PDF QA and Drive readback remain enforced.

### Calling by name
Run `python3 scripts/document_engineering/resolve_template.py --name "Salary Agreement"` or pass `{"template_id":"Salary Agreement", ...}` to the v3 renderer.
The name always resolves to the single current `salary-contract` source. An unknown or ambiguous name fails closed.

### Version pin and rollback
Git tag: `a9-enterprise-docs-v3.0.0`. Previous Git source and the original Drive archives remain immutable; roll back the active
registry through Git with a traced approval, never by deleting the historical sources.
