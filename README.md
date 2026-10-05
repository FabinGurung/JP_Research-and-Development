# JP Research and Development

Public research hub for Fabin Gurung's engineering R&D work.

## Canonical public architecture

```text
JP_Research-and-Development
├── R&D Home
├── AEC / Structural Research
│   ├── Thesis / database research
│   ├── methodology and shared-data reuse
│   ├── implementation evidence
│   ├── system/database graph
│   ├── preserved structural research demo
│   └── Structural Analysis → JP_Structural_Analysis
└── Hydropower Research
    ├── PhD research
    ├── hydrology / operations context
    ├── GIS / PHES research
    ├── database / schema views
    ├── Nepal hydropower map / source registries
    ├── case-study / proposal-defense material
    └── civil / structural research
```

The R&D repository is the **research publication hub**. Executable product engines live in their own repositories. In particular, the canonical structural-analysis/SAR product is **[JP_Structural_Analysis](https://github.com/FabinGurung/JP_Structural_Analysis)**.

## GitHub Pages production policy

There is exactly one canonical production source for this repository:

- branch: `main`
- workflow: `.github/workflows/deploy-pages.yml`
- environment: `github-pages`

Experimental, research, snapshot and solver branches may build and test, but must not be treated as production Pages owners. The production site must always open on the R&D Home and expose both AEC / Structural Research and Hydropower Research.

Expected site:

`https://fabingurung.github.io/JP_Research-and-Development/`

## Public/private boundary

GitHub Pages is public. Do not publish credentials, private Drive administration data, confidential project files, unsanitized client material, or unpublished engineering records.

## Development

The current site is a static-exported Next.js/React/TypeScript application. The production workflow installs the locked dependency set, runs repository verification, builds the static export, verifies the R&D routes, and deploys the generated `out/` artifact.
