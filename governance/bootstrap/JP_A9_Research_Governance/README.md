# JP A9 Research Governance

A small, Git-versioned control plane for research sequences. Google Drive remains the scientific-artifact authority. A7 indexes identities and routing; R&D presents approved research.

This is an empty bootstrap, not a migrated live ledger. Read CURRENT.json and sops/operation.md. Confirm a real repository ID and visibility before admitting live records.

## Validate

```sh
python -m pip install -r requirements.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

## Begin a provider-verified lane

Initialization fails until root CURRENT has ACTIVE status, a verified provider ID and verified PUBLIC/PRIVATE visibility. The tests use isolated synthetic fixtures; they do not provision a live project.

```sh
python scripts/a9.py init --project example-research-project --project-id PROJ-999999 --lane discussion
python scripts/a9.py append --project example-research-project --lane discussion --operation PRE --evidence pre.json
python scripts/a9.py resume --project example-research-project --lane discussion
```

The CLI prepares worktree changes; the caller commits them, reads the provider back, and attaches the actual receipt. It does not fabricate a provider ACK, tag, release, scientific observation or closure. `validate.py --base-ref <commit>` also rejects rewriting/removing already committed history.

Directories: schemas, sops, projects, events, releases, manifests, receipts, acknowledgements, readbacks, qa, workflows and scripts. Each project owns current.json, debt.json, artifact_edges.jsonl, drive_pointers.json, lanes, sequences and releases. Lane CURRENT is canonical; project CURRENT is a routing index.
