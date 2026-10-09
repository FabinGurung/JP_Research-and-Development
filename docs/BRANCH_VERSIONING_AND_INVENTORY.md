# R&D — complete Git branch inventory and versioning (2026-10-09)

The machine inventory [registry/branch-inventory.json](../registry/branch-inventory.json) was made from a fresh live GitHub branch API readback. Every observed branch has full SHA, name, status and grounded purpose, rather than an unverified claim that its contents are independently developed.

**Initial observed count: 100.** Classification: archive=49, production=1, researcher-template=33, website-marker=2, resource=14, snapshot=1.

## Branch naming and immutable snapshots

- `main`: **only** source for the unified GitHub Pages production deployment.
- `feature/<topic>-YYYYMMDD`: bounded code changes; branch refs cover the **entire repository**.
- `resource/<family>/<module>/vNNN-YYYYMMDD`: **versioned source release branch**. New version = new branch. Never force-push/overwrite an enumerated resource release.
- `snapshot/YYYYMMDD/<scope>/vNNN-<reason>`: immutable whole-repository rollback ref; version counter must increase within scope/date. Exact commit SHA remains the primary unambiguous rollback identifier.
- `archive/legacy-.../vNNN-YYYYMMDD`: descriptive alias refs to archived history, original legacy branches remain intact to avoid breaking links.
- `researcher/<slug>/{discussion,latex,presentation}`: legacy researcher workflow refs (33 placeholder/template commits). **Not** production website branches; actual admitted source and scientific QA must be established per project before any conversion.
- `researcher/fabin-gurung/website/<module>`: historical module refs; the canonical published code is the shared `main` website source.

A branch name is only a pointer; **the Git commit SHA and tagged/release manifest prove the exact version**. For reproducibility, each release should record SHA + manifest + build environment and its Drive output provider ID.

## What changed this run

- Protected pre-state: `snapshot/20261009/rnd-main/v001-pre-rose-dawn` (legacy HEAD). No old branch was force-updated, deleted or silently renamed.
- New Rose Dawn visual code and optional Dusk toggle on `main`; archived standalone research demos untouched.
- 14 `resource/**/v001-20261009` whole-repository versioned source baselines, each with `resource-branch.json`.
- Two clearer read-only aliases to archived source. These **are aliases**, not destructive Git branch renames.
- Central portal will render the entire observed inventory, descriptions and direct branch URLs.

## Compiling and releasing scientific outputs

A Git code change can trigger **source build/QA for a configured recipe**. It cannot responsibly produce a new scientific PDF for every commit when the LaTeX/Typst or presentation source is still Drive-only, missing, or lacks a reproducible recipe.

Desired admitted-release chain:

`GIT COMMIT → SOURCE/RECIPE VALIDATION → COMPILE → RENDER QA → GOOGLE DRIVE PDF/PPTX UPLOAD → DRIVE READBACK → RELEASE MANIFEST → LOCAL/MAIN LIBRARY GOVERNED ACK`

The R&D Pages website is built automatically from main by an existing passing GitHub Action. For thesis binaries, provider upload credentials, approved source recipes, font/toolchain licensing and researcher science QA must first be configured. Until then **NOT BUILT** is the accurate status, not completion.

We are not migrating old A9 private research corpora, altering Drive folder contents, deleting branches or updating other repositories in this workstream.
