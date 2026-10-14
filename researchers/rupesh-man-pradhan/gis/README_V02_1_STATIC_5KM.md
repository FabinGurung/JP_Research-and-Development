# Rupesh GIS — V02.1 static 5 km ward atlas

**Output:** [PNG, Drive](https://drive.google.com/file/d/1LPf032vcXFEdJ7GudGFvlQM1JrIWB8Gh/view) · **QA:** [Count CSV, Drive](https://drive.google.com/file/d/1xVA8wf30x_JGMIqVQNPSJfDdCPgl008I/view) · **Run receipt:** [Drive](https://drive.google.com/file/d/1btnjiCEofdGJ1Ml0_37y858zxX92Kqle/view)

The canonical executable script is `RMP_GIS_V02_1_STATIC_WARD_ATLAS.py` in the same folder. A Drive mirror of the locally executed script is [here](https://drive.google.com/file/d/1_7QlVkg-QsC4knBqZlfoulEMy1_9sNfJ/view), while the manuscript and research-original files remain in Drive. Older V02.0 source and original imagery are preserved as historical versions. No interactive map or new Colab notebook is required for this edition.

## Run locally, without Colab

Install `pip install numpy matplotlib shapely` and download these **input products** from Drive:

- [V02.0 full-resolution spatial join aggregated counts CSV](https://drive.google.com/file/d/1xVA8wf30x_JGMIqVQNPSJfDdCPgl008I/view)
- [V02.0-derived map-only ward geometry cache](https://drive.google.com/file/d/1OuxUmdXGTfJm2XVauYW7v9bbLdxEGqix/view)

Then run:

```bash
python researchers/rupesh-man-pradhan/gis/RMP_GIS_V02_1_STATIC_WARD_ATLAS.py \
  --geometry RMP_WARD_DISPLAY_GEOMETRY_CACHE_v0.2.1.json \
  --counts RMP_WARD_COUNTS_SPATIAL_VS_RECORDED_v0.2.0.csv \
  --out out
```

Output is a static **PNG** and a structured JSON receipt, not an HTML application. The script **only** reads the already-validated aggregate ward count CSV and generalized polygon geometry, then redraws the requested 5 km square frame. It does *not* recompute a geodesic buffer or rerun the point-in-polygon spatial join from the original 266 coordinates. The displayed 44.128 km side is **cartographic, approximate**, reconstructed from the preserved V02.0 map display cache; rerunning with exact original KLL geometry is required for a final precise geographic map frame. Previous full-resolution V02.0 spatial join supported 50 conflicts; those remain open.

## Standard ownership and versioning

**GitHub:** Python source, tests, README, source↔output manifest, commit history. **Google Drive:** original point workbook, researcher evidence, QA CSV, generalized boundary/cache, candidate PNG. No private building coordinates are checked into this public repository.

**Milestone:** frozen V01.4 tagged baseline; V02.0 and V02.1 are review candidates and are **not** retagged as approved results. The 33-ward historical boundary is not independently certified for a 2026 thesis map. Manual inclusion of the previously flagged Ward 33 record follows user approval without changing its observed latitude/longitude.

This is the general template for Binay/Rupesh scientific plotting: ordinary `.py` code, direct Python execution, static figures and provenance, optional Colab only for user-authorized cloud runtime or special authenticated GEE workflows.
