# Rupesh GIS V02.7 — OK-ward surveyed building locations

This edition generates a reproducible, **static thesis-style map** directly in Python. No Colab or image synthesis is used.

- Eleven wards marked `OK` in the non-engineered worksheet: 11, 21, 24, 25, 26, 27, 29, 30, 31, 32, 33
- Other wards are grey and no building coordinates from those wards appear
- 266 original points; 104 eligible by authoritative full-resolution spatial ward assignment
- **95 plotted** (50 engineered triangles, 45 non-engineered circles); **9 near-boundary points held** because the historical ward display geometry places them across the selected ward boundary
- Geographic location of the manually approved source anomaly remains unchanged and unplotted
- Source point coordinates are **not committed to this public repository**

The country/city boundaries originate in the uploaded national local-unit shapefile, in NepalDD/Everest datum, projected to UTM Zone 45N (EPSG:32645). Ward subdivisions use an earlier generalized display derived from Kathmandu Living Labs/OSM ward polygons. The ward polygon union matches the uploaded municipality to 98.52% area overlap, but this is not confirmation of the current official ward demarcation. A 5 km offset square extent, genuine transformed graticule and UTM-scaled 5 km scale bar are used.

## Reproducibility
Source: [RMP_GIS_V02_7_OK_WARDS_SURVEY_MAP.py](RMP_GIS_V02_7_OK_WARDS_SURVEY_MAP.py)

The script accepts six explicit arguments: `--xlsx`, `--points_csv`, `--join_csv`, `--municipality_shp`, `--ward_display_json`, and `--output_dir`. The original data must be fetched from the researcher's private Drive workspace. No silent corrections to source coordinates or ward assignments are permitted.

See [manifest](ok-wards-survey-map.v0.2.7.json) for exact source/output hashes, Drive file IDs, point counts and QA gate.

**[Static map in Drive](https://drive.google.com/file/d/1GZBgLjStrMe7sbyxp5WGcQh3GUdOr9oU/view)** · **[Source mirror](https://drive.google.com/file/d/1vo4X2roMb1S_eybQOilq4pD9s1PUMMhB/view)** · **[QA receipt](https://drive.google.com/file/d/1dbVMSV9QUXs2cdkyBxoAFgsnvcWof1An/view)** · **[Nine-point display hold](https://drive.google.com/file/d/1majfbUdYF0FDjruPhIksKz_HiYp6Dxpj/view)**

This Git revision controls the source; Google Drive remains source of truth for actual survey data and artifacts. This edition is registered for technical reproducibility, **not tagged as an approved scientific milestone**.
