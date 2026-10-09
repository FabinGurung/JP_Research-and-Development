# JP Research & Development — browser QA, refactor and research-search closeout
**Date:** 2026-10-09 (Asia/Kathmandu)  
**Scope:** GitHub repo/main source and public-safe static website only.  
**PRE main HEAD:** `3060c03431713a349a2469f41fd556520edec509`

## Phase 1 — actual browser QA
Added `.github/workflows/browser-qa.yml` and `scripts/browser_qa.cjs`. GitHub Actions installs real Chromium and runs DOM interactions + screenshots, desktop 1440×900, mobile 390×844 and narrow-width coverage, clipboard, reduced-motion, theme controls, keyboard, search and automated WCAG A/AA checks. Artifacts include screenshots, axe findings, machine JSON. Twelve base checks **passed** at [Actions 37927322585](https://github.com/FabinGurung/JP_Research-and-Development/actions/runs/37927322585). Expanded checks are subject to final HEAD CI validation; do not overclaim a passing run before reading it.

## Phase 2 — source modularization with route preservation
Extracted stable shell, evidence linking, escaping and write helpers to `scripts/site_core.py`, editorial home/start/owner pages to `scripts/site_pages.py`. Kept `scripts/build_site.py` as orchestrator and all legacy standalone demos unmodified. The refactored driver passed [repo validation](https://github.com/FabinGurung/JP_Research-and-Development/actions/runs/37927509368), [Pages deployment](https://github.com/FabinGurung/JP_Research-and-Development/actions/runs/37927509365), and [Chromium QA](https://github.com/FabinGurung/JP_Research-and-Development/actions/runs/37927509359).

## Phase 3 — research discovery
Added `scripts/site_search.py`, `web/search.js`, CSS and `search/index.html`; generated `data/research-index.json` from public-safe Git-owned researcher, branch and website metadata only. Enables collection filters, keyword scoring, query URL, keyboard / and Escape, and progressive result paging. Added source tests `scripts/test_site_search.py`. Fourteen browser checks passed for the search implementation at [Actions 37928546427](https://github.com/FabinGurung/JP_Research-and-Development/actions/runs/37928546427). Then improved responsive navigation with `web/menu.js` and added further mobile/browser tests, subject to final HEAD readback.

## Non-negotiable boundaries
- No database schema or DB migration.
- No Google Drive moves, renames, copies or folder changes.
- No A9 Local/Main read/write/ACK or researcher prompt dispatch.
- No scientific thesis content, code admission changes, new PDF renders, university approvals or supervisor sign-off.
- No force-pushing, branch deletion or history rewrite; commits advance HEAD only.
- Search index is **public discovery**, never an authoritative live provider mirror.
- Browser screenshot capture and axe automation **do not equal human aesthetic acceptance**. Screenshots can be reviewed in Actions artifacts.
- Preserve earlier source-audit HOLDs including RSH-004 root unverified and PU 144-rule production certification.

## Future safe boundary
Human screenshot/mobile QA; further modular extraction of specialized page renderers; verified route manifest. Researcher/database migrations happen only by later separate user trigger and exact authority.
