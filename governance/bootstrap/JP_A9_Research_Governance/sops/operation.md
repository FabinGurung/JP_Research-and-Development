# Bounded sequence protocol

1. Resolve provider identity, actual CURRENT and applicable lane policies; do not use prompt high-water marks as facts.
2. Capture PRE commit and scientific snapshot pointers before material mutation. A new sequence begins only with PRE.
3. Record snapshot/archive/enumeration and mutation operations. Corrections append SUPERSEDE; never edit existing events.
4. Hash and inventory actual artifacts. Unknown hashes and byte counts stay null; they do not prove release readiness.
5. POST carries QA evidence. Record actual provider readback and its receipt, ACK and registration.
6. CLOSE requires the same sequence to contain PRE, POST, provider readback, ACK and registration, all passing; no unresolved blocking debt. All scientific artifacts need verified hashes, sizes and reverse-reference receipts. A released event stays immutable.
7. Commit, provider-read back the resulting event and CURRENT, and write a separate external receipt. Do not claim that a content commit contains its own SHA.

The CLI checks worktree evidence references exist, refuses an unfinished sequence replay and produces deterministic resume pointers. The operator is responsible for the truth of provider receipt evidence. Local validation is not a substitute for remote readback. A crash between event and pointer writes fails validation; reconcile the committed event and pointer under a new correction before resuming.

Rollback preserves all historical events; an appended ROLLBACK_POINTER names a previously closed event within the same lane and opens explicit reconciliation debt. It never silently rewinds or closes a sequence. Review and resolve that debt before closure.

Use feature/<project>/<lane>/<sequence>; main is validated state. Milestone tags are immutable. Release metadata points to a content commit and provider receipts. Historical migration requires separate approval; start with one lane, not all histories.
