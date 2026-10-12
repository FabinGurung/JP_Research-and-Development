# Rupesh Man Pradhan / GIS V01.4 preview milestone

**Repository is public; original survey coordinates, research files, generated map and Colab outputs remain in Google Drive.**

This is a **Git-governed milestone source package** for the Rupesh GIS mapping lane. It records the last tested V01.4 implementation by exact provider file ID and SHA-256, without publicly copying any of the 266 building coordinates.

## Verified operational baseline

- Field source: 266 coordinate rows (150 engineered, 116 non-engineered).
- Pokhara main view: 265; Ward 33 anomalous coordinate remains separate/held.
- Standalone HTML inline renderer tested in a local browser; ward/category/outlier controls tested.
- Embedded Colab iframe was tested under local browser emulation.
- **Satellite/street basemap tiles have not been verified on the researcher's live network.** This is **NOT** an approved satellite-map release.
- Source CRS is presumed WGS84 based on decimal coordinates, **not independently certified**.
- Ward 30 cross-category coincident point requires human QA.

## Git / Drive division

Git owns this control, the executable notebook-extraction procedure and changes to release metadata. Google Drive owns the actual source workbook, the output-bearing Colab notebook, generated private map, QA checkpoint, and full scientific context. The stable Drive IDs and source SHA-256 are registered in [milestone.v0.1.4.json](milestone.v0.1.4.json).

**Now closed:** the complete runnable, output-stripped V01.4 notebook source is committed as [`RMP_GIS_V01_4_SOURCE_ONLY.ipynb`](RMP_GIS_V01_4_SOURCE_ONLY.ipynb). Its exact SHA-256 is pinned in the manifest and verified by release QA. It contains code, not saved outputs or the private researcher spreadsheet. The original output-bearing execution notebook remains in Drive.

## Release quality boundary

The version tag `rupesh-gis/v0.1.4-source`, if created and read back, denotes **repository provenance/QA candidate milestone**, not scientific approval and not a promise that tile servers work. GitHub Releases are project-wide Git snapshots; do not mistake the tag for an isolated researcher-only database.

CI tests the immutable manifest and extractor before tagging. The tag must not be re-pointed or substituted with a new branch. If tag/release cannot be created, the control must report `TAG_WRITE_UNAVAILABLE`, not claim success.

## Recovery

Use `python researchers/rupesh-man-pradhan/gis/source_snapshot.py path/to/downloaded_notebook.ipynb --output sanitized.ipynb` to verify the original output-bearing Drive bytes and create the source-only version. This never changes the Drive notebook. Copy only source-only code to Git after scientific/privacy review. The source spreadsheet stays private in Drive.

Do not create a new A9 Local/Main sequence just for Git-versioned source or metadata. A9 evidence and science admission remain separately governed.

Links: [Drive GIS folder](https://drive.google.com/drive/folders/1oIxLqgNrHiNq4HoFGoZNhFNfk5NwxdBt) | [Current Colab notebook](https://colab.research.google.com/drive/1xw37A932TR0jeTRyproLTCp5hu74skv4) | [Git/Drive authority](../../../docs/GIT_DRIVE_AUTHORITY_READ_FIRST.md)
