# Read first: Git version control and Drive evidence custody

**Effective 2026-10-11. Scope: FabinGurung/JP_Research-and-Development source and its Git-managed academic thesis/presentation systems, including Safal Dawadi.** This is an explicit user-approved change. This scoped policy replaces the version-control instructions that repeatedly advanced A9 Drive Local/Main sequence counters. Do not apply it to unrelated A9 business/finance workflows without separate governance.

## Authorities
- GitHub: exact PRE/POST commit SHA, branches/PRs, source/config/versioned manifests, QA checks, approved tags/releases. See [machine contract](../controls/git-drive-authority.json).
- Google Drive: canonical original research records, private site data and photos, source-admission/project metadata, licensed fonts, Google Docs, PDFs and PPTX deliverables. Git manifests store their exact provider IDs, not files.
- Scientific and format approval: official program/source controls, actual admitted evidence, researcher/supervisor. Git or a generated deck is not scientific approval.

## Mandatory workflow
1. Read this document and the current machine contract on GitHub main, the researcher workspace, and current Drive source/format records.
2. Capture verified current SHA as PRE, commit changes non-force to Git and obtain POST SHA + CI evidence. Preserve historical Git refs.
3. Build from current researcher source; verify provenance and visually check outputs. Store deliverables in Drive and read back IDs/checksums.
4. Update typed Git artifact manifest/release index. Use release tags only when approved and verified as created. Never claim an uncreated tag.
5. Do not create Drive snapshot copies or increment Drive Local/Main for routine Git-versioned changes. For separately authorized physical storage moves or scientific-source edits, follow their applicable Drive preservation controls and document why.
6. Never import private photos, personal secrets or licensed fonts into public Git. Never use old chat memory as source authority.

## Safal historical boundary
Safal old Local Library: [sheet](https://docs.google.com/spreadsheets/d/10g8-tr417XltYDbk2yItEZjrJ_2xdT7pbPlJgUI8MYo/edit), historical last seq **20**. Main Library: [registry](https://docs.google.com/spreadsheets/d/18NE0GIbw0lDDlrIcflGS3_VccDZ2LZn1FoPbebSc71o/edit), last actual ack **5**. Seq **6–20** remain historic but unacknowledged. They are not implicitly synced, canceled or scientifically approved. Do NOT generate Seq21 for another PPTX/code change. See [immutable legacy-index snapshot](../registry/legacy-a9-ledger-index.json).

Safal v0.9 source commit: `9036ed6bd3ab9b4d2628380e331df02cc05cc974` on `safal/presentation/v0.9-methodology-flow-20261010`. PDF Drive `1WWb8Jf9Aq3IpHvY1H8tn2nVqpgKGy7dY`; PPTX Drive `1LpQD2cehoUwmIzwTzC2dfjELS5OGfehj`.

## Cross-location trace
- [Drive migration decision](https://docs.google.com/document/d/1CYzEnpPDyPSLXwGq8LG1auckd_qiHoreGZ9jiWvki3Q/edit)
- [Drive previous-state snapshots](https://drive.google.com/drive/folders/1YyXg_-MvTzbzAIzikaM7__tysPqi469J)
- [Migration event](../registry/migrations/git-drive-authority-20261011.json)
- [Presentation shared tower](../controls/presentation/tower.json)
- [Safal researcher handover](../researchers/safal-dawadi/presentation/GOVERNANCE_READ_FIRST.md)

**Collision rule:** if an earlier Drive Read First says `PUSH_OR_PULL_ON_DEMAND` for Safal version-only work, do not reactivate the old counter. The newer scoped Git cutover governs versions; old A9 quality/evidence and scientific admission requirements still apply. Do not resolve an actual source or format conflict by guessing; surface it.
