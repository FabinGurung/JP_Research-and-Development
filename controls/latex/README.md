# JP R&D shared LaTeX control tower · 1.2.0

**Operational owner:** R&D GitHub `main`; **global router:** A7; **original academic authority:** approved PU format v1.13 and thesis-wide Drive v1.23; **project scientific authority:** researcher/source manifest.

This is a **selective public-safe executable bridge**, **not** a certified replacement for the full Drive rules or private A9 libraries. Read `format-authorities.json` first, then `pu-msc-format.rules.json`, `build-contract.json`, `qa-contract.json`, `release-contract.json`, and `migration-status.json`. Use the researcher's own configuration only after those shared controls.

## Inheritance

A7 bootstrap → `A7_MODULE.json` → `controls/latex.control.json` → this package → researcher `control.json` → admitted manuscript → source-level XeLaTeX/Biber build → independent technical/render/scientific gates → Drive PDF readback → separately governed A9 Local/Main registration.

## Rules

- No global bibliography default. Select IEEE, Harvard or APA 7 explicitly per project.
- Exact Times New Roman is required for production; never publish font binaries or private manuscript data in Git.
- Do not edit compiled PDFs; edit source and regenerate.
- No automatically certified scientific, format or publication success from a passing source gate.
- Cite Drive originals, keep stable IDs and previous releases. Unmapped PU rules remain authoritative at the Drive source.

[PU original](https://docs.google.com/document/d/1FjbNdNN_Fb_tKoapaYHW2jLoEF9lqxrYPYrCwTi87Ys/edit) · [Thesis tower](https://docs.google.com/document/d/1jc6WIqXbAixAYYndeB2Idw59fAzjBbnDKlq49THeu_A/edit) · [R&D source-control contract](../latex.control.json).

## Current scoped status

Shared infrastructure prepared; complete rule parity, Safal source admission, private exact-font build and A9 release are **HOLD**. See `migration-status.json`.
