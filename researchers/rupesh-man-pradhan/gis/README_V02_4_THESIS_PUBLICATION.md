# Rupesh GIS V02.4 — static thesis ward-count plate

This edition is reproducible Python cartography, distinct from image-based design mockups.

## Published products
- [300-dpi static PNG in Google Drive](https://drive.google.com/file/d/1eadHA4d5qUb68t8H2n7-ji4226VCzMah/view)
- [Full research-data and reproducibility package in Google Drive](https://drive.google.com/file/d/1_qLe5Er9IEqxM2X-Uptktx54YtM2Gn0L/view)
- [Python mirror in Google Drive](https://drive.google.com/file/d/1DTdtVOdjbCQdrJ4YeB5LNhJ1UCdyyC8p/view)
- [Researcher figure handoff and source boundaries](https://docs.google.com/document/d/1QWfTPK9TMCKp0tdZjSql3pcgZhiskmMNE8K3R3G9HDM/edit)

## Computation

The original V02.0 full-resolution geographic join assigned building coordinates to Pokhara's historical 33-ward polygons. This publication edition draws **only spatially assigned ward counts** and generalized ward display geometry; no new point-in-polygon operation is performed. The 50 records with mismatching entered ward labels are counted in the geometrically matched ward. The user-approved Ward 33 out-of-polygon input remains in the Ward 33 aggregate as a **manual exception**, not as a fabricated geometric match.

Counts: 266 total (150 engineered, 116 non-engineered). 27 wards with both categories are colored and labeled with a blue engineered number and an orange non-engineered number. The map has no ward IDs within the polygons, and no private survey markers.

## Geographic reference
- WGS84 / UTM 45N EPSG:32645; fixed square map frame, minimum 5-km margin, side approximately 44.128 km.
- Pokhara ward polygons: historic Kathmandu Living Labs / OpenStreetMap layer. Their current official status is not established.
- National locator: actual Natural Earth 1:110m Nepal country outline, indicative Pokhara extent.

## Reproduce

From the Drive ZIP, in an environment with geopandas, pandas, matplotlib, numpy, shapely and pyproj:

```bash
python RMP_GIS_V02_4_THESIS_WARD_PLATE.py \
  --counts RMP_WARD_COUNTS_SPATIAL_VS_RECORDED_v0.2.0.csv \
  --geometry RMP_WARD_DISPLAY_GEOMETRY_CACHE_v0.2.1.json \
  --nepal NEPAL_NATURAL_EARTH_110M_LOCATOR.geojson \
  --png RMP_POKHARA_WARD_SPATIAL_COUNTS_THESIS_PLATE_v0.2.4.png \
  --receipt RMP_GIS_V02_4_REPRODUCIBILITY_RECEIPT.json
```

Source and output SHA-256 hashes, data IDs, figure dimensions, and exceptions are in [manifest](static-ward-publication.v0.2.4.json). No raw building locations or private workbook entries are committed to public Git.

## Version-control scope

Code edition V02.4 is controlled by this Git commit, not a new A9 main-library sequence. The frozen V01.4 milestone and V02.0-V02.3 history remain unchanged. This code commit is **not** a claim of final scientific boundary certification or manuscript admission. Those decisions belong to the researcher.
