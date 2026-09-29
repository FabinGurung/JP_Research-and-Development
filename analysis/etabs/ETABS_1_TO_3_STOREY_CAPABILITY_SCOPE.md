# ETABS-equivalent 1–3 storey building check — validated scope

## Purpose

Define what can be reproduced independently with OpenSeesPy / Python, what can be automated through the ETABS OAPI when ETABS is available, and what must not be claimed without an actual ETABS design run.

## A. Structural analysis that can be reproduced independently now

For a conventional 1–3 storey beam-column building model, the following can be implemented and checked with OpenSeesPy/Python from explicit geometry, material, section, support, mass and load inputs:

- geometry, connectivity and boundary-condition validation;
- dead/live/member/wall load bookkeeping;
- linear static gravity and lateral analysis;
- support reactions and global equilibrium;
- beam/column axial force, shear and bending moment extraction;
- storey displacement and inter-storey drift;
- eigenvalue/modal analysis: periods, frequencies, mode shapes and modal properties;
- response-spectrum analysis with explicit spectrum input and scripted modal combination;
- P-Delta second-order analysis;
- nonlinear static/pushover analysis after hinge/fiber assumptions are explicitly defined;
- linear/nonlinear time-history analysis after ground-motion and damping assumptions are explicitly defined;
- cross-checks against hand calculations, moment distribution, stiffness-method calculations or exported ETABS tables.

These are analysis checks, not automatic adoption of ETABS proprietary design results.

## B. Work that can be automated in actual ETABS when ETABS is installed/licensed

ETABS exposes an OAPI that can be scripted from a Windows environment. A controlled automation lane can:

- start or attach to ETABS;
- initialize/create a model;
- define materials and frame sections;
- create joints, beams, columns and area objects;
- assign restraints, diaphragms and loads;
- define load cases and combinations;
- save the `.edb` model;
- run analysis;
- read analysis results;
- start concrete frame design/check;
- retrieve beam design summary results;
- retrieve column PMM/shear design summary results;
- export/import `.e2k` and database tables where supported by the installed ETABS release.

A true ETABS run therefore requires a Windows machine on which the licensed ETABS application and its API are available. The current GitHub/ChatGPT runtime does not contain the proprietary ETABS executable.

## C. Boundary that must not be blurred

OpenSees is not a drop-in replacement for ETABS concrete-design modules. It can independently reproduce the structural response and can support our own code-check calculations, but an "ETABS design result" (required reinforcement, PMM ratio, joint/shear design output, ETABS warnings, ETABS solver log, etc.) must come from an actual ETABS run or from an ETABS-exported result table.

## D. Minimum 1–3 storey QA sequence

1. Units and coordinate system.
2. Grid, storey elevations and connectivity.
3. Material properties and section properties.
4. Supports, releases, offsets and diaphragm assumptions.
5. Slab/wall/member load transfer assumptions.
6. Self weight, dead load, live load and other gravity loads.
7. Mass source.
8. Seismic/wind parameters and governing code inputs.
9. Load patterns, load cases and load combinations.
10. Linear-static equilibrium check.
11. Beam/column force sanity checks.
12. Modal periods, mode shapes and mass participation.
13. Response-spectrum/base-shear checks when required.
14. Storey displacement and inter-storey drift.
15. P-Delta/second-order sensitivity when required.
16. Beam flexure/shear design check under the chosen code.
17. Column axial-flexure (PMM) and shear check under the chosen code.
18. Strong-column/weak-beam and joint checks where required by the chosen seismic code/system.
19. Foundation reactions exported for footing/foundation checks.
20. Cross-solver comparison: ETABS ↔ OpenSeesPy ↔ hand/independent calculation for selected control cases.

## E. Inputs required before a specific building can be checked

- number of storeys (1, 2 or 3) and storey heights;
- plan/grid dimensions;
- beam/column/slab/wall dimensions;
- concrete/rebar grades and other materials;
- support/foundation idealization;
- gravity loads and wall loads;
- diaphragm/slab modeling choice;
- seismic/wind location and code parameters;
- design code and structural system;
- any existing ETABS `.edb`, `.e2k`, Excel/database-table export, screenshots or analysis/design report available for comparison.

## F. Current validation status

The first OpenSeesPy control case for the thesis `SAMPLE_MDM_001` runs successfully under OpenSeesPy 3.8.0.0 / OpenSees 3.8.0. Member-end moments reproduce the stored MDM values exactly. The stored reactions do not match the independently solved beam reactions and are therefore flagged for governed data reconciliation rather than silently changed.
