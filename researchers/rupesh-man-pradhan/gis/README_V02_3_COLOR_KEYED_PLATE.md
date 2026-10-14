# Rupesh GIS V02.3 — color-keyed thesis plate

This is a **static figure and source-code milestone**, not an approved scientific map. The Python source is version-controlled in GitHub; the exported 300-dpi PNG is retained in Google Drive.

- [PNG (Google Drive)](https://drive.google.com/file/d/1jllWxqUewK3gmViVZ3gol2OIRYSSg9Fu/view)
- [Python source (Drive mirror)](https://drive.google.com/file/d/1kMg1BC1ilKZUSQnrNCddLr9q--9bpKj4/view)
- [Original V02.1 Git source](RMP_GIS_V02_1_STATIC_WARD_ATLAS.py)
- [Input counts/QA (Drive)](https://drive.google.com/file/d/1xVA8wf30x_JGMIqVQNPSJfDdCPgl008I/view)

Run locally with the V02.1 generalized display cache and V02.0 full-resolution spatial-join summary:

```bash
python RMP_GIS_V02_3_COLOR_KEYED_THESIS_PLATE.py \
 --geometry RMP_WARD_DISPLAY_GEOMETRY_CACHE_v0.2.1.json \
 --counts RMP_WARD_COUNTS_SPATIAL_VS_RECORDED_v0.2.0.csv \
 --output RMP_POKHARA_WARD_COLOR_KEY_THESIS_PLATE_v0.2.3.png
```

The output has 27 qualifying wards and preserves the 5-km minimum margin around the municipality. Individual ward colors are cross-referenced to a count key; blue numbers indicate engineered counts and orange indicate non-engineered counts. Small wards use leader-line ward-number callouts instead of crowding labels. No building point locations appear.

**QA limitations**: historical KLL/OSM boundary authority, 50 mismatches between field-ward labels and polygon membership, one user-approved Ward 33 geographic exception. The Nepal inset is only a coarse country locator. The cached display polygons must not be reused for any new point-in-polygon calculation. This is a **review candidate**, not a frozen publication-admission release.

Version-control principle: Git controls the code and manifest; Drive controls original data and image outputs. V01.4 tag remains immutable, and V02.0, V02.1, V02.2 remain preserved. No A9 Local/Main sequence is advanced for routine code changes.
