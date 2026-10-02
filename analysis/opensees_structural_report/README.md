# OpenSees Structural Analysis Report lane

This lane is intentionally separate from the thesis MDM validation lane and the research/nonlinear reproduction lane.

## Purpose

Build a governed pipeline for real project structural-analysis reports:

Google Drive source authority -> deterministic E2K inventory/parser -> normalized structural database -> DB-to-OpenSeesPy translator -> OpenSees analyses -> normalized results -> design/check layer -> report renderer -> Drive evidence package.

## Data boundary

Client/project source files and source-derived normalized models remain in governed Google Drive. Do not commit raw E2K/EDB files, client drawings, private reports, or project-specific normalized geometry to this public repository unless explicitly approved.

The repository contains reusable parser/validator/solver/report code plus synthetic tests only.

## Current R0/R1 status

- Dedicated branch created: `opensees-structural-report-v0.1`
- First governed pilot selected: Sabitri Giri residence
- Existing report-template reference: Hari Om Dhaubanjar structural analysis report
- Actual Sabitri E2K source has been read and hashed in the governed Drive lane
- Deterministic E2K inventory parser is implemented here
- Report blueprint v0.1 is defined here
- OpenSeesPy is pinned for the next translator/solver stage

## Guardrails

1. Raw Drive authority is never silently mutated.
2. ChatGPT orchestrates, documents and performs QA; OpenSees is the numerical solver.
3. ETABS-only design outputs (for example proprietary PMM/design ratios) are not represented as independent OpenSees results unless separately recalculated by an explicit design module.
4. Unknown E2K records are preserved by source hash/section inventory and must not be silently discarded.
5. A report sentence derived from analysis should ultimately trace to a normalized result row, analysis-run identity, model hash and source authority.
