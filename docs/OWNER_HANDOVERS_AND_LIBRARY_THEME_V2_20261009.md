# R&D owner-only handovers and Living Research Library v2 — 2026-10-09

## Scope

This is an additive GitHub main development series, NOT a bulk Drive migration or scientific thesis revision. Main PRE: `6c732afe0b8290096baaa3c7f073068d3c7e3aca`. Later commits must be resolved from provider; never guess POST SHA in self-referential markdown.

### Three deliveries

1. **Execution system**: `controls/researcher-migration-rules.json`, `registry/researcher-migration-status.json`, `schemas/researcher-migration-status.schema.json`, `prompts/researcher_owner_execution_master.md`, `scripts/researchers/generate_prompts.py`. Trigger = user paste in owning researcher thread ONLY. ZERO deletes and no automatic Main ACK.
2. **11 generated prompts**: `prompts/researchers/RSH-001__fabin-gurung.md` through `RSH-011__sunil-rana.md`, exact registered IDs and formerly verified Drive folders, RSH-004 root HOLD; `python3 scripts/researchers/generate_prompts.py --check` deterministically guards drift. Individual researcher scientific source is NOT edited centrally.
3. **Living Research Library**: `web/living-hero.html` (self-contained illustrated flying book), responsive CSS, simple JavaScript day/night and pause/reduced-motion; `owner-prompts/` static page with eleven copy controls and Git source links. Three.js deliberately not needed: CSS scene has no third-party/CDN download, lower dependency risk and reduced-motion support. Existing A7, research lanes and demos remain in place.

### Per-researcher execution boundaries

The owner receives exact prompt only when user pastes it. The owner must fresh-read Drive, confirm its authority and exact root ID, choose minimal safe changes, provider PRE, reversible low-risk changes, provider POST, A9 Local registration and separate Main sync. High/unknown risks HOLD. Do not delete/trash; do not mass-create folders; do not modify research conclusions, source originals or external/shared folders. The central status registry records **not triggered** for all eleven, not an event log of live executions.

### Validation and work not asserted

Git repository CI must pass, Pages deployment must succeed; historical Git branches preserved and no new release tag claimed. Website animation is progressive and pure CSS; screenshot/real-device visual QA remains separate. No individual Drive relocation or archiving, no A9 Local/Main writes, no automatic PDF compile, no PU 144-rule certification, no scientific sign-off. The named earlier skeleton ZIP content remains separately unverified in this chat.
