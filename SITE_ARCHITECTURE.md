# Site architecture — research foundation v3.0.0

The static Next.js 16 App Router renders the R&D hub from local approved data. There is no backend or browser fetch of private scientific authorities. GitHub Actions builds `out/` and publishes only main.

## Directory

`data/research-projects.json` carries permanent project IDs, unique slugs, labels, short scope summaries and publication routes. The server-rendered directory and static project pages consume the same records. Every title rename retains identity; slug changes require an alias/redirect. No dataset/manuscript status is inferred from directory metadata.

| Route | Purpose |
|---|---|
| `/` | Research hub and established modules |
| `/projects/` | Cross-project directory |
| `/projects/[slug]/` | Static project identity and public research links |
| `/governance/` | Record responsibilities and foundation status |
| `/aec/` | Existing structural/database research overview |
| `/hydropower/` | Existing energy research overview |
| `/hydropower/proposal-defense/` | Existing proposal-defense presentation |
| `/research`, `/system`, `/prototype`, `/workflow`, `/evidence`, `/roadmap`, `/thesis`, `/graph` | Preserved AEC thesis presentation routes |

The existing public static methodology, structural solver, hydropower data, schema, graph and map pages remain in `public/`. Research product engines continue to live in specialist repositories. The structural analysis link still resolves to JP_Structural_Analysis.

## Navigation and accessibility

The hub navigation includes the directory and record-responsibility page. AEC routes keep their established module navigation. Internal links use sitePath for the Pages base path. Directory cards are ordinary keyboard-focusable links; project fields use definition lists; responsibility tables have captions and scoped headers. Cards collapse naturally to one column on small screens. Existing navigation retains touch and keyboard scrolling, focus visibility and reduced-motion support.

## Existing scientific presentation

The curated AEC data, 80 graph nodes, 106 relationships and 10 sanitized evidence PNGs are preserved. The graph is a client-side presentation with keyboard/text alternatives; it does not become a live database. This rebuild introduces no numerical research claims.

## Governance foundation

`governance/ADR-001-research-authority-boundaries.md` defines A7/A9/R&D/Drive responsibilities, migration, rollback, privacy, release strategy and resume rules. The nested A9 repository package is an empty deployment foundation. The nested template remains BOOTSTRAP_NOT_PROVISIONED; the public foundation is already adopted within this existing R&D repository. A separate private deployment is optional. No detailed live A9 ledger belongs in R&D.

## Checks and release lineage

Feature and PR CI run source/security/graph/solver/type/directory checks, A9 schema and state-machine tests, a static build and Pages-output verification. A PRE branch preserves each prior provider head. Source manifests cover every tracked payload and exclude generated output, caches, dependencies and archives. Provider readback and CI evidence are recorded separately from the content commit to avoid circular SHA assertions.
