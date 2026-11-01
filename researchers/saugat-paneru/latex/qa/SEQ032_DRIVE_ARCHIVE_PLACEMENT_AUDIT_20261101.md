# Saugat Paneru — historical archive placement audit (2026-11-01)

**Scope:** RSH-002 Google Drive folder organization only. This record does not publish private file IDs or content and does not modify scientific data, the manuscript, or production revision identities.

**Governing policy:** A7 Permanent live IDs & version control, `registry/curations/memory-live-version-control.v0.1.json`, collection `A7-MEM-LIVE-VERSION-009`. Same original live file ID, enumerated archives in dedicated history folders, rollback into original identities. Reference PR: A7 #100 (merged). This was a location-only change; it is **not** a new LATEX_SEQ and does not require creating additional PRE/POST copies.

## Provider-grounded decisions

- Saugat `production-current.json` on GitHub main identifies user-designated CURRENT `LATEX_SEQ031_R2`, its permanent PDF and complete ZIP IDs and the separate permanent checkpoint and native Doc IDs.
- `LATEX_SEQ032` remains a draft candidate (PR #120) with independent font, Doc-parity and academic signoff gates.
- The existing `03_LATEX_PROJECT/ARCHIVE__SAUGAT_SEQ031_R2_PRE_SEQ032__20261101` already held fourteen numbered PRE snapshots (unchanged).
- The existing `08_WORK_CHECKPOINTS/HISTORY` already held older checkpoint and historical chat/archive records; reused this folder.
- Added a single supporting-history subfolder inside the existing SEQ031 R2 PRE archive; no duplicate top-level version archive or replacement live provider object was created.

## Readback-proven move register

| Classification | Before | After | Count | Verification |
|---|---|---|---:|---|
| Post checkpoint, edit-source fragments and QA evidence | `03_LATEX_PROJECT/CURRENT__SAUGAT_SEQ031_R2_20261101/` | `03_LATEX_PROJECT/ARCHIVE__SAUGAT_SEQ031_R2_PRE_SEQ032__20261101/SUPPORTING_HISTORY__SEQ031_R2_POST_QA_EDIT_SOURCE__20261101/` | 11 | All 11 Drive move responses showed the new sole parent; destination list returned exactly 11 |
| Historical PRE checkpoint records and other historical checkpoint references | `08_WORK_CHECKPOINTS/CURRENT/` | `08_WORK_CHECKPOINTS/HISTORY/` | 10 | All 10 Drive move responses showed the new sole parent; destination-list sample included the moved records |
| Historical CP98–CP111 checkpoint folders (including old source candidate and WORKING names) | `08_WORK_CHECKPOINTS/CURRENT/` | `08_WORK_CHECKPOINTS/HISTORY/` | 14 | All 14 Drive move responses showed the new sole parent; final HISTORY listing count increased to 95 |

**Total existing provider objects moved: 35.** Move method: `files.update` with `addParents=verified_destination` and `removeParents=verified_source` only; no binary byte uploads, content replacement, renames, deletes, permission edits or recreated live file IDs.

## Final production and checkpoint invariants

- `03_LATEX_PROJECT/CURRENT__SAUGAT_SEQ031_R2_20261101/`: exactly **2** objects, the original SEQ031 R2 PDF and complete LaTeX ZIP.
- `08_WORK_CHECKPOINTS/CURRENT/`: exactly **1** object, `CURRENT_CHECKPOINT`.
- `03_LATEX_PROJECT/ARCHIVE__SAUGAT_SEQ031_R2_PRE_SEQ032__20261101/`: original 14 enumerated PRE snapshots plus one supporting history subfolder (15 entries); all 14 PRE IDs remain unchanged.
- Supporting-history subfolder: **11** moved evidence objects.
- `08_WORK_CHECKPOINTS/HISTORY/`: **95** historical entries after the latest moves.
- Permanent native Google Doc remains in its original separate owner folder, with previously noted content-parity HOLD unchanged.
- `LATEX_SEQ032` is still a candidate. No CURRENT release promotion occurred.

**Integrity/QA limitation:** Provider ID and parent/location readback succeeded. The contents themselves were not rehashed after these metadata-only moves. Independent thesis academic signoff, full format QA and source parity are not implied.

**Restoration:** Historical files and folders retain their original Drive object IDs; an authorized folder-layout rollback moves the same IDs back to their former parents. An authorized content rollback separately restores a selected PRE snapshot's bytes into the original PDF/ZIP/Doc/checkpoint live IDs; archive objects must not become replacement live authorities.

**Historical traceability:** exact per-object old and new parent/ID pairs were verified through connected Google Drive move results. Keep provider-private identifiers in its permissioned Drive records; this public Git audit intentionally references folder names and counts only.
