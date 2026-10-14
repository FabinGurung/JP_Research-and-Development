# Rupesh GIS V02.0 — Pokhara dual-category ward-summary map

**Working edition, not a tagged scientific release.** Derived from immutable [Rupesh GIS V01.4 source milestone](https://github.com/FabinGurung/JP_Research-and-Development/releases/tag/rupesh-gis/v0.1.4-source).

Source notebook: [RMP_GIS_V02_WARD_SUMMARY_SOURCE_ONLY.ipynb](RMP_GIS_V02_WARD_SUMMARY_SOURCE_ONLY.ipynb). It reads the pinned private Drive-normalized CSV using Google OAuth, fetches an open Kathmandu Living Labs/OSM 33-ward layer, and generates a 100-km-buffered square map frame with a ward detail inset. It includes no individual building records or output cells in this **public** Git repository.

**Reviewer preview:** [Interactive map in Drive](https://drive.google.com/file/d/1HWoibIKXp4pN2rPvVTRLPbtKhB6b7cL6/view) · [Static map](https://drive.google.com/file/d/1VCU2mkAJVP9_NZ99zABt9aQ4GZ083-07/view) · [QA workbook](https://drive.google.com/file/d/1k1aFgh3l0okVU0svWsWKCEoPsyeIS7pu/view) · [Colab](https://colab.research.google.com/drive/1goAh_Sc6eNdVGkjam5tuh7PghtMf62rd).

**Exact QA:** 266 original records; 150 engineered, 116 non-engineered; 27 of 33 wards qualify under full polygon overlay. The original recorded-ward column *also* yields 27 qualifying wards but a different set: spatial includes W20, recorded includes W05. 50 rows disagree between source ward and polygon ward. The user-approved anomalous W33 row remains counted in W33, with no invented coordinate correction.

**Boundary limitation:** 33 polygons originated in Kathmandu Living Labs historical OSM dataset. It is open mapping evidence, *not* newly certified 2026 government ward geometry. Projected analysis EPSG:32645; coordinate-source datum assumed EPSG:4326. The map shows only aggregated counts, not individual coordinates.

**Version control:** Git owns notebook source and this manifest; Google Drive owns private input and generated results. No new routine A9 Local/Main counter or Drive snapshot was created. This is a **working v0.2.0 source commit**, with a release tag intentionally withheld until geography, data and scientific QA gates close.

Machine manifest: [ward-summary.v0.2.0.json](ward-summary.v0.2.0.json). Run `python researchers/rupesh-man-pradhan/gis/validate_ward_summary_source.py` to check the source notebook without accessing private data.
