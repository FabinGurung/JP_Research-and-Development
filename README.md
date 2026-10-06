# JP Research and Development

Cross-project research publication hub for theses, AEC studies, energy investigations and future R&D.

- [Research directory](https://fabingurung.github.io/JP_Research-and-Development/projects/): five stable project addresses.
- Existing AEC / Structural and Hydropower modules, technical graphs and demonstrations remain available.
- `data/research-projects.json` owns public directory metadata. Permanent PROJ IDs survive title changes.
- `CURRENT.json` owns this repository's bounded publication state and explicit dependencies.

## Responsibilities

| Layer | Role |
|---|---|
| A7 | Identities, authority routing and public relationships |
| A9 | Detailed sequence governance after dedicated repository provisioning |
| R&D | Understandable public research presentation |
| Drive | Original scientific artifacts and working documents |
| Specialist repositories | Executable product engines |

Read `governance/ADR-001-research-authority-boundaries.md`. The standalone A9 foundation is prepared at `governance/bootstrap/JP_A9_Research_Governance`; it is not an active second ledger. This existing repository is the adopted location for the public foundation; a separate private A9 repository is optional. No scientific history, manuscript state or private Drive references were imported. Saugat Discussion and LaTeX execution belongs in a separate chat.

## Development and validation

```sh
npm ci
npm run test:pages
python -m pip install -r governance/bootstrap/JP_A9_Research_Governance/requirements.txt
npm run verify:governance
NEXT_PUBLIC_BASE_PATH=/JP_Research-and-Development GITHUB_PAGES=true npm run build
NEXT_PUBLIC_BASE_PATH=/JP_Research-and-Development npm run verify:pages-output
```

The static Next.js export produces `out/`. Main is the sole production source; `.github/workflows/deploy-pages.yml` publishes through the github-pages environment. Feature/PR CI validates the site and governance bootstrap without deploying it. The pinned lockfile is retained and installed with npm ci.

Public Pages excludes private evidence and restricted research content. Directory entries identify projects; publication pending does not imply scientific completion.
