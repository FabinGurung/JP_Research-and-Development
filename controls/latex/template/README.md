# One reusable R&D LaTeX template — no copies

Authoritative global governance: [../tower.json](../tower.json). Actual shared typography is [pumlsc-shared.sty](pumlsc-shared.sty).

Every researcher loads the same style from this path using `\\usepackage{pumlsc-shared}` in their admitted `main.tex`. The build launcher adds this directory to the TeX search path (`TEXINPUTS`); do **not** copy the shared style into a researcher workspace. `main.example.tex` is an illustrative skeleton only, **not** an approved PU front matter or a published manuscript.

The shared style currently implements a small common baseline (A4, margins, exact font requirement, 12pt via documentclass, 1.5 spacing, no global indent, Roman/Arabic helper commands). All remaining university-format requirements still require separate review against the approved Drive v1.13 original. No full certified PU template claim is made.

Project-scoped extensions may only be introduced by a central, numbered amendment (101 onward) and entry in `../extension-registry.json`; source files then live under `researchers/<slug>/latex/extensions/`, never as a copied base style.

The generic template includes no private fonts, university logo bytes, manuscript prose, scientific figures, bibliography default or private researcher identifiers.
