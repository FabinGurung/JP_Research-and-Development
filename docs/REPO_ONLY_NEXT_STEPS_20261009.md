# R&D repository-only improvements — October 9, 2026

## Explicit scope lock

**Allowed now:** GitHub repository code, static website, usability, source-only validation, documentation, portable scripts, CI and governance metadata. **Deferred:** database migrations, Drive moves/renames/archives, cross-researcher scientific content, A9 Local/Main writes, new scientific PDF builds, PU university-format signoff. User must trigger each researcher-specific migration by pasting its complete own handover in that researcher's chat.

## Completed in this repository-only phase

1. Created `scripts/validate_site_links.py` with offline generated-site link and static asset checking. It excludes preserved historical research demos and follows only local links; tests in `scripts/test_site_links.py`.
2. Enforced these tests in repository validator and both GitHub Pages/CI build workflows, without requiring database/network access.
3. Added a human-friendly `start-here/` public operating guide with links to Git source, code QA, shared controls, migrations deferred, owner-prompt copies and current Actions runs.
4. Corrected stale 2026-10-09 Safal status copy to identify historical review decisions without claiming later scientific approval or newer A9 Main synchronization. Revised `CURRENT.json` portal-code labels; archived source facts and external Drive pointers preserved.

## Next repository-only improvements, prioritized

- **P1:** Independent screenshot/mobile/keyboard test of homepage, owner handover copy pages, theme contrast and motion settings. GitHub CI static tests do not replace browser QA.
- **P2:** Improve source-level test isolation and clear typed parsers for large `scripts/build_site.py`; preserve existing routes and the six legacy site modules.
- **P3:** Introduce generated status pages only where the exact source of truth is stable. Do not claim live GitHub/Drive status from a dated static JSON.
- **P4:** Improve master README onboarding, information architecture, search/navigation and researcher authority links. No new control tower.
- **P5:** Apply future shared LaTeX bugfixes only with canonical one-template rule review and regression evidence. Do not trigger any PDF builds from unrelated website commits.

## Proof and non-claims

PRE = the Git commit before each bounded change; POST = non-forced commit. Green Actions validates code/links and deploys a static site, not scientific approval. A9 registrations, Main ACK, PU full 144-rule certification, individual owner migrations and authorized PDF production remain their own governed workstreams. Never delete historical refs or scientific evidence.
